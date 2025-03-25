from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class UserSearchResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Contact Request schemas
class ContactRequestCreate(BaseModel):
    to_user_id: int

class ContactRequestResponse(BaseModel):
    id: int
    from_user: UserSearchResponse
    to_user: UserSearchResponse
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Special schema for the frontend that expects a 'from_user' field
class ContactRequestWithUserResponse(BaseModel):
    id: int
    from_user: UserSearchResponse
    
    class Config:
        orm_mode = True

# Contact schemas
class ContactResponse(BaseModel):
    id: int
    contact: UserSearchResponse
    created_at: datetime

    class Config:
        orm_mode = True

# Message schemas
class MessageCreate(BaseModel):
    receiver_id: Optional[int] = None
    group_id: Optional[int] = None
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: Optional[int] = None
    group_id: Optional[int] = None
    content: str
    encrypted: bool
    delivered: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Group schemas
class GroupCreate(BaseModel):
    name: str

class GroupAddMember(BaseModel):
    user_id: int

class GroupResponse(BaseModel):
    id: int
    name: str
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class GroupMemberResponse(BaseModel):
    id: int
    user: UserSearchResponse

    class Config:
        orm_mode = True

class GroupWithMembersResponse(GroupResponse):
    members: List[GroupMemberResponse]

    class Config:
        orm_mode = True

# Notification schemas
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    content: str
    read: bool
    related_user_id: Optional[int] = None
    related_group_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True 