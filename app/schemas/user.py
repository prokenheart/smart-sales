from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_account: str
    user_password: str

class UserCreate(UserBase):
    pass

class UserIdPath(BaseModel):
    user_id: uuid.UUID

class UserEmailQuery(BaseModel):
    user_email: EmailStr

class UserResponse(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_account: str
    user_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdateInfo(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_phone: Optional[str] = None

class UserUpdatePassword(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)