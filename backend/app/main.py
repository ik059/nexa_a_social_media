from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import text

app = FastAPI(
    title="Next Social Media app",
    description="Backend for nexa",
    version="0.1.0"
)

@app.get('/')
async def root():
    return {
        "message":"This is nexa app APIs"
    }
    
@app.get('/test-db')
async def test_db(db : AssertionError = Depends(get_db)):
    result = await db.execute(text('SELECT 1'))
    return {"db_status": result.scalar()}
    