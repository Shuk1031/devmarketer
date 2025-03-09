from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.post import Platform, PostStatus


class PostVariantBase(BaseModel):
    content: str


class PostVariantCreate(PostVariantBase):
    pass


class PostVariantInDB(PostVariantBase):
    id: int
    post_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostVariant(PostVariantInDB):
    """PostVariant schema to return to client"""
    pass


class PostBase(BaseModel):
    platform: Platform
    scheduled_at: Optional[datetime] = None


class PostCreate(PostBase):
    title: str
    keywords: List[str]


class PostSchedule(BaseModel):
    scheduled_at: datetime
    variant_id: int


class PostInDB(PostBase):
    id: int
    user_id: int
    status: PostStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Post(PostInDB):
    """Post schema to return to client"""
    variants: List[PostVariant] = []


class PublishResponse(BaseModel):
    status: str
    sns_response: dict