from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base, TimeStampedModel


class Engagement(Base, TimeStampedModel):
    __tablename__ = "engagements"

    post_variant_id = Column(Integer, ForeignKey("post_variants.id"), nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    comments = Column(Integer, default=0, nullable=False)
    shares = Column(Integer, default=0, nullable=False)  # RTs in Twitter
    upvotes = Column(Integer, default=0, nullable=False)  # For Reddit, PH
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    variant = relationship("PostVariant", back_populates="engagements")