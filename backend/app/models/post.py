import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Post(Base):
    __tablename__ = "posts"
    
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    
    user = relationship("User", back_populates='posts')
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comments", back_populates="post", cascade="all, delete-orphan")
