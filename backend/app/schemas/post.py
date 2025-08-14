from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class PostBase(BaseModel):
    content: str
    
class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: UUID
    user_id:UUID
    created_at : datetime
    
    class Config:
        orm_mode = True