from sqlalchemy.ext.asyncio import create_async_engine,  AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

database_url = settings.DATABASE_URL

engine = create_async_engine(database_url, echo = True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit= False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session