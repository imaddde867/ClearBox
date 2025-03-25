from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Group, GroupMember, Contact, Notification
from ..schemas import GroupCreate, GroupResponse, GroupAddMember, GroupWithMembersResponse, GroupMemberResponse
from ..security import get_current_active_user
from ..routes.websockets import manager

router = APIRouter(tags=["Groups"])

@router.post("/group", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new group
    """
    # Create the group
    db_group = Group(
        name=group.name,
        creator_id=current_user.id
    )

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    # Add the creator as a member automatically
    group_member = GroupMember(
        group_id=db_group.id,
        user_id=current_user.id
    )

    db.add(group_member)
    db.commit()

    return db_group

@router.post("/group/{group_id}/add", response_model=GroupWithMembersResponse)
def add_member_to_group(
    group_id: int,
    member: GroupAddMember,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Add a contact to a group
    """
    # Check if the group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Check if the current user is the creator or a member
    is_creator = group.creator_id == current_user.id
    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first() is not None

    if not is_creator and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a group member to add contacts"
        )

    # Check if the user to add exists
    user_to_add = db.query(User).filter(User.id == member.user_id).first()
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if the user is already in the group
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == member.user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this group"
        )

    # Check if the user is a contact
    contact = db.query(Contact).filter(
        Contact.user_id == current_user.id,
        Contact.contact_id == member.user_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add your contacts to a group"
        )

    # Add the user to the group
    group_member = GroupMember(
        group_id=group_id,
        user_id=member.user_id
    )

    db.add(group_member)
    
    # Create a notification for the added user
    notification = Notification(
        user_id=member.user_id,
        type="group_invite",
        content=f"{current_user.username} added you to group: {group.name}",
        read=False,
        related_user_id=current_user.id,
        related_group_id=group_id
    )
    db.add(notification)
    db.commit()
    
    # Notify the user if they are online
    if manager.is_user_online(member.user_id):
        notification_message = {
            "type": "notification",
            "notification_type": "group_invite",
            "group_id": group_id,
            "group_name": group.name,
            "sender_id": current_user.id,
            "sender_name": current_user.username,
            "timestamp": notification.created_at.isoformat()
        }
        background_tasks.add_task(
            manager.send_personal_message,
            notification_message,
            member.user_id
        )

    # Return the updated group with members
    return get_group_with_members(group_id, db)

@router.get("/groups", response_model=List[GroupResponse])
def get_user_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all groups the user belongs to
    """
    # Get groups where user is the creator
    created_groups = db.query(Group).filter(Group.creator_id == current_user.id).all()

    # Get groups where user is a member
    member_of_groups = db.query(Group).join(GroupMember).filter(
        GroupMember.user_id == current_user.id
    ).all()

    # Combine and deduplicate
    all_groups = list({group.id: group for group in created_groups + member_of_groups}.values())

    return all_groups

@router.get("/group/{group_id}/members", response_model=List[GroupMemberResponse])
def get_group_members(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all members of a specific group
    """
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Check if user is a member or creator
    is_creator = group.creator_id == current_user.id
    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first() is not None

    if not is_creator and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a group member to view members"
        )

    # Get all members
    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).all()

    return members

@router.get("/group/{group_id}", response_model=GroupWithMembersResponse)
def get_group_detail(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get detailed information about a group including members
    """
    # Check if group exists
    group = get_group_with_members(group_id, db)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Check if user is a member or creator
    is_creator = group.creator_id == current_user.id
    is_member = any(member.user.id == current_user.id for member in group.members)

    if not is_creator and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a group member to view details"
        )

    return group

def get_group_with_members(group_id: int, db: Session):
    """Helper function to get a group with its members"""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return None

    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).all()

    group.members = members
    return group

@router.delete("/group/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a group (only the creator can do this)
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    if group.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the group creator can delete the group"
        )
        
    # Get all members to notify them
    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    member_ids = [member.user_id for member in members if member.user_id != current_user.id]
    
    # Delete all members first (due to foreign key constraints)
    db.query(GroupMember).filter(GroupMember.group_id == group_id).delete()

    # Delete the group
    db.delete(group)
    db.commit()
    
    # Notify all members that the group was deleted
    for member_id in member_ids:
        # Create a notification
        notification = Notification(
            user_id=member_id,
            type="group_deleted",
            content=f"Group '{group.name}' has been deleted by {current_user.username}",
            read=False,
            related_user_id=current_user.id
        )
        db.add(notification)
        
        # Send real-time notification if user is online
        if manager.is_user_online(member_id):
            notification_message = {
                "type": "notification",
                "notification_type": "group_deleted",
                "group_id": group_id,
                "group_name": group.name,
                "sender_id": current_user.id,
                "sender_name": current_user.username,
                "timestamp": notification.created_at.isoformat()
            }
            background_tasks.add_task(
                manager.send_personal_message,
                notification_message,
                member_id
            )
    
    db.commit()

    return {"detail": "Group successfully deleted"}

@router.delete("/group/{group_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
def leave_group(
    group_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Leave a group (members can leave, creators cannot leave - they must delete)
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Creators cannot leave their own groups - they must delete them
    if group.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group creators cannot leave. You must delete the group instead."
        )

    # Check if the user is a member
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not a member of this group"
        )

    # Remove the user from the group
    db.delete(membership)
    db.commit()
    
    # Notify the group creator
    notification = Notification(
        user_id=group.creator_id,
        type="group_member_left",
        content=f"{current_user.username} left the group: {group.name}",
        read=False,
        related_user_id=current_user.id,
        related_group_id=group_id
    )
    db.add(notification)
    db.commit()
    
    # Send real-time notification to the creator if online
    if manager.is_user_online(group.creator_id):
        notification_message = {
            "type": "notification",
            "notification_type": "group_member_left",
            "group_id": group_id,
            "group_name": group.name,
            "user_id": current_user.id,
            "user_name": current_user.username,
            "timestamp": notification.created_at.isoformat()
        }
        background_tasks.add_task(
            manager.send_personal_message,
            notification_message,
            group.creator_id
        )

    return {"detail": "Successfully left the group"}