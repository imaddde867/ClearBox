from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse, UserUpdate, UserSearchResponse
from ..security import get_current_active_user, create_token, get_password_hash

router = APIRouter(tags=["Users"])

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user (sign up)
    """
    # Check if the username or email already exists
    existing_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the new user
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/users/me", response_model=UserResponse)
def get_current_user(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the current user's information
    """
    return current_user

@router.get("/users/search", response_model=List[UserSearchResponse])
def search_users(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search for users by username or full name
    """
    if len(q) < 2:
        return []

    search_term = f"%{q}%"
    users = db.query(User).filter(
        or_(
            User.username.ilike(search_term),
            User.full_name.ilike(search_term)
        ),
        User.id != current_user.id  # Exclude current user
    ).limit(10).all()

    return users

@router.put("/users/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update the current user's information
    """
    # Update user fields
    if user_update.username is not None and user_update.username != "":
        # Check if username is already taken
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        current_user.username = user_update.username

    if user_update.email is not None and user_update.email != "":
        # Check if email is already taken
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email

    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name

    if user_update.bio is not None:
        current_user.bio = user_update.bio

    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url

    # If password is provided, update it
    if user_update.password is not None and user_update.password != "":
        current_user.password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)

    return current_user