from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from app.db.session import Base
import enum


class AuthProvider(enum.Enum):
    GITHUB = "github"
    TWITTER = "twitter"
    GOOGLE = "google"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    auth_provider = Column(Enum(AuthProvider), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
