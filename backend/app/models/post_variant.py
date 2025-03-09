from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base, TimeStampedModel


class PostVariant(Base, TimeStampedModel):
    __tablename__ = "post_variants"

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(Text, nullable=False)
    
    # Relationships
    post = relationship("Post", back_populates="variants")
    engagements = relationship("Engagement", back_populates="variant", cascade="all, delete-orphan")