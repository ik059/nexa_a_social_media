from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token, LoginData
from app.models.user import User
from app.core.security import hash_password, create_access_token, verify_password
from app.db.session import get_db
from app.api.deps import get_current_user

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

@router.post('/login', response_model=Token)
async def login(login_data: LoginData, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Username or Password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    token = create_access_token({'sub':str(user.id)})
    return {
        "access_token":token,
        "token_type":'bearer'
    }
    
@router.get('/me')
async def read_user_me(current_user: User = Depends(get_current_user)):
    print(current_user)
    return current_user