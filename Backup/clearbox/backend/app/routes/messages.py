from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import and_, or_, desc

from ..database import get_db
from ..models import User, Message, Contact, Group, GroupMember, Notification
from ..schemas import MessageCreate, MessageResponse
from ..security import get_current_active_user
from ..encryption import encrypt_message, decrypt_message
from ..mqtt_client import publish_message, get_mqtt_client
from .websockets import manager

router = APIRouter(tags=["Messages"])

def send_mqtt_message(topic: str, message_data: dict):
    """Background task to send message via MQTT"""
    publish_message(topic, message_data)

@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Send a message to a user or group
    """
    # Handle direct message
    if message.receiver_id is not None:
        # Check if the receiver exists
        receiver = db.query(User).filter(User.id == message.receiver_id).first()
        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receiver not found"
            )
        
        # Check if users are contacts
        contact = db.query(Contact).filter(
            Contact.user_id == current_user.id,
            Contact.contact_id == message.receiver_id
        ).first()
        
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only send messages to your contacts"
            )
        
        # Encrypt the message content
        encrypted_content = encrypt_message(message.content)
        
        # Check if recipient is online
        recipient_online = manager.is_user_online(message.receiver_id)
        
        # Create the message in the database
        db_message = Message(
            sender_id=current_user.id,
            receiver_id=message.receiver_id,
            content=encrypted_content,
            encrypted=True,
            # Set delivered to True if recipient is online, otherwise False
            delivered=recipient_online
        )
        
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # If recipient is online, send via WebSocket
        if recipient_online:
            # Send message via WebSocket
            ws_message = {
                "type": "message",
                "messageId": db_message.id,
                "senderId": db_message.sender_id,
                "content": message.content,  # Send decrypted content
                "timestamp": db_message.created_at.isoformat()
            }
            
            # Send in background to avoid blocking
            background_tasks.add_task(
                manager.send_personal_message,
                ws_message,
                message.receiver_id
            )
        else:
            # Recipient is offline, create a notification for them
            notification = Notification(
                user_id=message.receiver_id,
                type="message",
                content=f"New message from {current_user.username}",
                read=False,
                related_user_id=current_user.id
            )
            db.add(notification)
            db.commit()
        
        # Return the message with decrypted content for the sender
        response = db_message
        response.content = message.content  # Return original content to sender
        return response
    
    # Handle group message
    else:
        # Check if the group exists
        group = db.query(Group).filter(Group.id == message.group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        
        # Check if user is a member of the group
        member = db.query(GroupMember).filter(
            GroupMember.group_id == message.group_id,
            GroupMember.user_id == current_user.id
        ).first()
        
        if not member and group.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group"
            )
        
        # Encrypt the message content
        encrypted_content = encrypt_message(message.content)
        
        # Create the message in the database
        db_message = Message(
            sender_id=current_user.id,
            group_id=message.group_id,
            content=encrypted_content,
            encrypted=True,
            # Group messages are considered delivered when sent
            delivered=True
        )
        
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # Get all group members
        members = db.query(GroupMember).filter(
            GroupMember.group_id == message.group_id
        ).all()
        
        # Prepare message for WebSocket
        ws_message = {
            "type": "group_message",
            "messageId": db_message.id,
            "senderId": db_message.sender_id,
            "groupId": db_message.group_id,
            "content": message.content,  # Send decrypted content
            "timestamp": db_message.created_at.isoformat()
        }
        
        # Send to all online members
        for member in members:
            if member.user_id != current_user.id:  # Don't send to sender
                if manager.is_user_online(member.user_id):
                    # Send in background to avoid blocking
                    background_tasks.add_task(
                        manager.send_personal_message,
                        ws_message,
                        member.user_id
                    )
                else:
                    # Create notification for offline members
                    notification = Notification(
                        user_id=member.user_id,
                        type="group_message",
                        content=f"New message in {group.name} from {current_user.username}",
                        read=False,
                        related_user_id=current_user.id,
                        related_group_id=group.id
                    )
                    db.add(notification)
        
        # Commit all notifications
        db.commit()
        
        # Return the message with decrypted content for the sender
        response = db_message
        response.content = message.content  # Return original content to sender
        return response

@router.get("/messages/user/{user_id}", response_model=List[MessageResponse])
def get_user_messages(
    user_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get messages exchanged with a specific user
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if users are contacts
    contact = db.query(Contact).filter(
        Contact.user_id == current_user.id,
        Contact.contact_id == user_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view messages with your contacts"
        )
    
    # Get messages between users (sent and received)
    messages = db.query(Message).filter(
        or_(
            and_(
                Message.sender_id == current_user.id,
                Message.receiver_id == user_id
            ),
            and_(
                Message.sender_id == user_id,
                Message.receiver_id == current_user.id
            )
        ),
        Message.group_id == None
    ).order_by(desc(Message.created_at)).limit(limit).all()
    
    # Decrypt message content for display
    for msg in messages:
        if msg.encrypted:
            try:
                msg.content = decrypt_message(msg.content)
            except Exception:
                # If decryption fails, indicate that
                msg.content = "[Encrypted message]"
        
        # Mark as delivered if received and the current user is the receiver
        if msg.sender_id == user_id and msg.receiver_id == current_user.id and not msg.delivered:
            msg.delivered = True
            db.commit()
    
    return messages

@router.get("/messages/group/{group_id}", response_model=List[MessageResponse])
def get_group_messages(
    group_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get messages from a specific group
    """
    # Check if the group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if user is a member of the group
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not member and group.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )
    
    # Get messages from the group
    messages = db.query(Message).filter(
        Message.group_id == group_id
    ).order_by(desc(Message.created_at)).limit(limit).all()
    
    # Decrypt message content for display
    for msg in messages:
        if msg.encrypted:
            try:
                msg.content = decrypt_message(msg.content)
            except Exception:
                # If decryption fails, indicate that
                msg.content = "[Encrypted message]"
    
    return messages

@router.put("/messages/{message_id}/delivered")
def mark_message_delivered(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Mark a message as delivered (for tracking read/unread messages)
    """
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or you're not the receiver"
        )
    
    message.delivered = True
    db.commit()
    
    return {"status": "success"}

@router.post("/messages/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message_endpoint(
    message_data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Send a message to a user or group using a simplified endpoint
    """
    # Check if to_user_id or group_id is provided
    to_user_id = message_data.get("to_user_id")
    group_id = message_data.get("group_id")
    content = message_data.get("content")
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required"
        )
    
    # Create a MessageCreate object
    message = MessageCreate(
        receiver_id=to_user_id,
        group_id=group_id,
        content=content
    )
    
    # Pass to the main send_message function
    return send_message(message, background_tasks, db, current_user)

@router.get("/messages/{user_id}", response_model=List[MessageResponse])
def get_chat_messages(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get messages exchanged with a specific user (alias for get_user_messages)
    """
    return get_user_messages(user_id, 50, db, current_user) 