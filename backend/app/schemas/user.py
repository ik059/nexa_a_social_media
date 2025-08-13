from pydantic import BaseModel, EmailStr
import uuid

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
class UserOut(UserBase):
    id: uuid.UUID
    is_active : bool
    
    class Config:
        orm_mode = True
    