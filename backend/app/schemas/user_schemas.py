from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import AuthProvider


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    auth_provider: AuthProvider


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: int
    auth_provider: AuthProvider
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """User schema to return to client"""
    pass