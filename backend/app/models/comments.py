import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Comments(Base):
    __tablename__ = 'comments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id'), nullable=False)
    comment = Column(Text, nullable=False)
    commented_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
