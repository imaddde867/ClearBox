from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_, and_
import logging

from ..database import get_db
from ..models import User, ContactRequest, Contact, Notification
from ..schemas import (
    UserSearchResponse,
    ContactRequestCreate,
    ContactRequestResponse,
    ContactResponse,
    UserResponse,
    ContactRequestWithUserResponse,
)
from ..security import get_current_active_user

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Contacts"])

@router.get("/search", response_model=List[UserSearchResponse])
def search_users(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Search for users by username or email
    """
    search_query = f"%{query}%"
    users = db.query(User).filter(
        or_(
            User.username.ilike(search_query),
            User.email.ilike(search_query)
        ),
        User.id != current_user.id
    ).all()
    
    return users

@router.post("/contact/request", status_code=status.HTTP_201_CREATED, response_model=ContactRequestResponse)
def create_contact_request(
    contact_request: ContactRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Send a contact request to another user
    """
    # Check if the target user exists
    to_user = db.query(User).filter(User.id == contact_request.to_user_id).first()
    if not to_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if a request already exists
    existing_request = db.query(ContactRequest).filter(
        ContactRequest.from_user_id == current_user.id,
        ContactRequest.to_user_id == contact_request.to_user_id
    ).first()
    
    if existing_request:
        if existing_request.status == "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact request already sent and pending"
            )
        elif existing_request.status == "accepted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Users are already contacts"
            )
        # If denied, we allow sending a new request
        else:
            existing_request.status = "pending"
            db.commit()
            db.refresh(existing_request)
            return existing_request
    
    # Check if there's a request in the other direction
    reverse_request = db.query(ContactRequest).filter(
        ContactRequest.from_user_id == contact_request.to_user_id,
        ContactRequest.to_user_id == current_user.id
    ).first()
    
    if reverse_request:
        if reverse_request.status == "pending":
            # Auto-accept if there's a pending reverse request
            reverse_request.status = "accepted"
            db.commit()
            
            # Create mutual contacts
            contact1 = Contact(user_id=current_user.id, contact_id=contact_request.to_user_id)
            contact2 = Contact(user_id=contact_request.to_user_id, contact_id=current_user.id)
            db.add(contact1)
            db.add(contact2)
            db.commit()
            
            # Create a new accepted request in this direction too
            new_request = ContactRequest(
                from_user_id=current_user.id,
                to_user_id=contact_request.to_user_id,
                status="accepted"
            )
            db.add(new_request)
            db.commit()
            db.refresh(new_request)
            return new_request
        elif reverse_request.status == "accepted":
            # Already contacts, check if we need to create a record in this direction
            existing_contact_record = db.query(ContactRequest).filter(
                ContactRequest.from_user_id == current_user.id,
                ContactRequest.to_user_id == contact_request.to_user_id,
                ContactRequest.status == "accepted"
            ).first()
            
            if not existing_contact_record:
                new_request = ContactRequest(
                    from_user_id=current_user.id,
                    to_user_id=contact_request.to_user_id,
                    status="accepted"
                )
                db.add(new_request)
                db.commit()
                db.refresh(new_request)
                return new_request
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Users are already contacts"
                )
    
    # Create new contact request
    new_request = ContactRequest(
        from_user_id=current_user.id,
        to_user_id=contact_request.to_user_id,
        status="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return new_request

@router.get("/contact/requests", response_model=List[ContactRequestResponse])
def get_pending_contact_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all pending contact requests for the current user
    """
    requests = db.query(ContactRequest).filter(
        ContactRequest.to_user_id == current_user.id,
        ContactRequest.status == "pending"
    ).all()
    
    return requests

@router.post("/contacts/accept/{request_id}", response_model=ContactRequestResponse)
@router.post("/contact/accept/{request_id}", response_model=ContactRequestResponse)
def accept_contact_request_by_id(
    request_id: int,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Accept a contact request by its ID
    """
    logger.info(f"User {current_user.id} accepting contact request {request_id}")
    
    request = db.query(ContactRequest).filter(
        ContactRequest.id == request_id,
        ContactRequest.to_user_id == current_user.id,
        ContactRequest.status == "pending"
    ).first()
    
    if not request:
        logger.warning(f"Contact request {request_id} not found or not pending for user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact request not found or not pending"
        )
    
    # Update request status
    request.status = "accepted"
    db.commit()
    
    # Create mutual contacts
    contact1 = Contact(user_id=current_user.id, contact_id=request.from_user_id)
    contact2 = Contact(user_id=request.from_user_id, contact_id=current_user.id)
    db.add(contact1)
    db.add(contact2)
    db.commit()
    
    # Create a corresponding accepted request in the other direction
    reverse_request = db.query(ContactRequest).filter(
        ContactRequest.from_user_id == current_user.id,
        ContactRequest.to_user_id == request.from_user_id
    ).first()
    
    if not reverse_request:
        reverse_request = ContactRequest(
            from_user_id=current_user.id,
            to_user_id=request.from_user_id,
            status="accepted"
        )
        db.add(reverse_request)
        db.commit()
    else:
        reverse_request.status = "accepted"
        db.commit()
    
    # Create a notification for the request sender
    if background_tasks:
        from_user = db.query(User).filter(User.id == request.from_user_id).first()
        notification = Notification(
            user_id=request.from_user_id,
            content=f"{current_user.username} accepted your contact request",
            type="contact_accepted"
        )
        db.add(notification)
        db.commit()
    
    logger.info(f"Contact request {request_id} accepted successfully")
    db.refresh(request)
    return request

@router.post("/contacts/reject/{request_id}", response_model=ContactRequestResponse)
@router.post("/contact/deny/{request_id}", response_model=ContactRequestResponse)
def reject_contact_request_by_id(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reject a contact request
    """
    logger.info(f"User {current_user.id} rejecting contact request {request_id}")
    
    request = db.query(ContactRequest).filter(
        ContactRequest.id == request_id,
        ContactRequest.to_user_id == current_user.id,
        ContactRequest.status == "pending"
    ).first()
    
    if not request:
        logger.warning(f"Contact request {request_id} not found or not pending for user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact request not found or not pending"
        )
    
    # Update request status
    request.status = "denied"
    db.commit()
    db.refresh(request)
    
    logger.info(f"Contact request {request_id} rejected successfully")
    return request

@router.get("/contacts", response_model=List[UserResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all contacts for the current user
    """
    contacts = db.query(User).join(
        Contact, 
        Contact.contact_id == User.id
    ).filter(
        Contact.user_id == current_user.id
    ).all()
    
    return contacts

@router.get("/contacts/requests", response_model=List[ContactRequestWithUserResponse])
def get_contact_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all contact requests for the current user
    """
    # Get contact requests and the associated user information
    requests = db.query(ContactRequest).join(
        User,
        User.id == ContactRequest.from_user_id
    ).filter(
        ContactRequest.to_user_id == current_user.id,
        ContactRequest.status == "pending"
    ).all()
    
    # Format the response to match what the frontend expects
    response = []
    for request in requests:
        response.append({
            "id": request.id,
            "from_user": request.from_user
        })
    
    return response

@router.get("/contacts/sent-requests", response_model=List[UserResponse])
def get_sent_contact_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all contact requests sent by the current user
    """
    # Get users to whom the current user has sent contact requests
    requests = db.query(User).join(
        ContactRequest,
        ContactRequest.to_user_id == User.id
    ).filter(
        ContactRequest.from_user_id == current_user.id,
        ContactRequest.status == "pending"
    ).all()
    
    return requests

@router.post("/contacts/request/{user_id}", status_code=status.HTTP_201_CREATED)
def send_contact_request(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Send a contact request to another user
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if the user is not trying to add themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot add yourself as a contact"
        )
    
    # Check if they are already contacts
    existing_contact = db.query(Contact).filter(
        and_(
            Contact.user_id == current_user.id,
            Contact.contact_id == user_id
        )
    ).first()
    
    if existing_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already in your contacts"
        )
    
    # Check if there is already a pending request
    existing_request = db.query(ContactRequest).filter(
        and_(
            ContactRequest.from_user_id == current_user.id,
            ContactRequest.to_user_id == user_id,
            ContactRequest.status == "pending"
        )
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already sent a request to this user"
        )
    
    # Create the contact request
    contact_request = ContactRequest(
        from_user_id=current_user.id,
        to_user_id=user_id,
        status="pending"
    )
    
    db.add(contact_request)
    
    # Create a notification for the recipient
    notification = Notification(
        user_id=user_id,
        type="contact_request",
        content=f"{current_user.username} sent you a contact request",
        related_user_id=current_user.id
    )
    
    db.add(notification)
    db.commit()
    
    return {"status": "success"}

@router.post("/contacts/accept/{user_id}")
def accept_contact_request(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Accept a contact request from a user
    """
    # Check if the request exists
    request = db.query(ContactRequest).filter(
        and_(
            ContactRequest.from_user_id == user_id,
            ContactRequest.to_user_id == current_user.id,
            ContactRequest.status == "pending"
        )
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact request not found"
        )
    
    # Update the request status
    request.status = "accepted"
    
    # Create contacts for both users
    contact1 = Contact(
        user_id=current_user.id,
        contact_id=user_id
    )
    
    contact2 = Contact(
        user_id=user_id,
        contact_id=current_user.id
    )
    
    db.add(contact1)
    db.add(contact2)
    
    # Create a notification for the sender
    notification = Notification(
        user_id=user_id,
        type="contact_accepted",
        content=f"{current_user.username} accepted your contact request",
        related_user_id=current_user.id
    )
    
    db.add(notification)
    db.commit()
    
    return {"status": "success"}

@router.post("/contacts/reject/{user_id}")
def reject_contact_request(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reject a contact request from a user
    """
    # Check if the request exists
    request = db.query(ContactRequest).filter(
        and_(
            ContactRequest.from_user_id == user_id,
            ContactRequest.to_user_id == current_user.id,
            ContactRequest.status == "pending"
        )
    ).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact request not found"
        )
    
    # Update the request status
    request.status = "rejected"
    db.commit()
    
    return {"status": "success"}

@router.delete("/contacts/{user_id}")
def remove_contact(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Remove a user from contacts
    """
    # Delete the contact relationship in both directions
    db.query(Contact).filter(
        and_(
            Contact.user_id == current_user.id,
            Contact.contact_id == user_id
        )
    ).delete()
    
    db.query(Contact).filter(
        and_(
            Contact.user_id == user_id,
            Contact.contact_id == current_user.id
        )
    ).delete()
    
    db.commit()
    
    return {"status": "success"}

# Keep the existing endpoints but have them call the new unified handlers
@router.post("/contact/accept/{request_id}", response_model=ContactRequestResponse, include_in_schema=False)
def accept_contact_request_legacy(
    request_id: int,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Legacy endpoint for accepting a contact request"""
    return accept_contact_request_by_id(request_id, background_tasks, db, current_user)

@router.post("/contact/deny/{request_id}", response_model=ContactRequestResponse, include_in_schema=False)
def deny_contact_request_legacy(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Legacy endpoint for denying a contact request"""
    return reject_contact_request_by_id(request_id, db, current_user) 