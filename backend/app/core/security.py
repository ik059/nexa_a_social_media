from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash_password(password :str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM )