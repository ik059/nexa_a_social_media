from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.like import Like
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.like import LikeCreate, LikeRead
import uuid

router = APIRouter(prefix="/likes", tags=['Likes'])

@router.post('/likepost', response_model=LikeRead)
async def like_post(
    like_in: LikeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_like = Like(
        id= str(uuid.uuid4()),
        user_id = current_user.id,
        post_id = like_in.post_id
    )
    
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like)
    return new_like