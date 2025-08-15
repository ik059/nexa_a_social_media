from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
class LikeCreate(BaseModel):
    post_id: UUID

class LikeRead(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    liked_at: datetime
    
    class Config:
        orm_mode = True