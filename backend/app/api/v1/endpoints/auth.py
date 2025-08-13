from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.core.security import hash_password, create_access_token
from app.db.session import get_db

router = APIRouter()

@router.post('/register', response_model = UserOut)
async def register(user_in:UserCreate, db: AsyncSession = Depends(get_db)):
    print(user_in)
    result = await db.execute(select(User).where((User.email == user_in.email) | (User.username == user_in.username)))
    exist_user = result.scalar_one_or_none()
    if exist_user:
        raise HTTPException(status_code=400, detail="Email or username already exist")
    
    new_user = User(
        username = user_in.username,
        email = user_in.email,
        hashed_password = hash_password(user_in.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user