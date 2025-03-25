from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Group, GroupMember, Contact
from ..schemas import GroupCreate, GroupResponse, GroupAddMember, GroupWithMembersResponse
from ..security import get_current_active_user

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
    db.commit()

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

    # Delete all members first (due to foreign key constraints)
    db.query(GroupMember).filter(GroupMember.group_id == group_id).delete()

    # Delete the group
    db.delete(group)
    db.commit()

    return {"detail": "Group successfully deleted"}