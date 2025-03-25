from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse, Token, UserLogin
from ..security import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    db_user_by_username = db.query(User).filter(User.username == user.username).first()
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists
    db_user_by_email = db.query(User).filter(User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Add an alias for the signup endpoint
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (alias for signup)
    """
    return signup(user, db)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/email", response_model=Token)
def login_with_email(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password, returns a token
    """
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile
    """
    return current_user

@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Delete current user account (GDPR compliance)
    """
    db.delete(current_user)
    db.commit()
    return {"detail": "User successfully deleted"}