from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
class CommentCreate(BaseModel):
    post_id: UUID
    comment: str
    
class CommentRead(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    comment: str
    commented_at: datetime
    