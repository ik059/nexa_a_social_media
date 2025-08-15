from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comments import Comments
from app.models.user  import User
from app.schemas.comment import CommentCreate, CommentRead
from app.api.deps import get_current_user
from app.db.session import get_db
import uuid

router = APIRouter(prefix='/comments', tags=['Comments'])

@router.post("/commentpost", response_model=CommentRead)
async def addComments(
    comment_in: CommentCreate,
    current_user : User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_comment = Comments(
        id = str(uuid.uuid4()),
        user_id = current_user.id,
        post_id= comment_in.post_id,
        comment = comment_in.comment
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment