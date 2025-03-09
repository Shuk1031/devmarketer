from sqlalchemy import Column, String, ForeignKey, DateTime, Enum, Integer
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, TimeStampedModel


class Platform(enum.Enum):
    X = "x"
    REDDIT = "reddit"
    PRODUCTHUNT = "producthunt"


class PostStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class Post(Base, TimeStampedModel):
    __tablename__ = "posts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    scheduled_at = Column(DateTime, nullable=True)
    status = Column(Enum(PostStatus), default=PostStatus.DRAFT, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="posts")
    variants = relationship("PostVariant", back_populates="post", cascade="all, delete-orphan")


# Add relationship to User model
from app.models.user import User
User.posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")