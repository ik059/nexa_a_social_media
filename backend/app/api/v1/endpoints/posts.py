from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from app.db.session import get_db
from app.schemas.post import PostCreate, PostRead
from app.models.post import Post
from app.models.user import User
from app.api.deps import get_current_user
from uuid import UUID

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post('/createpost', response_model= PostRead)
async def create_post(
    post_in: PostCreate,
    current_user : User =  Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_post = Post(
        content = post_in.content,
        user_id = current_user.id
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post
@router.get('/getallpost', response_model=List[PostRead])
async def get_all_post(
    current_user:User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user:
        result = await db.execute(select(Post).order_by(Post.created_at.desc()))
        posts = result.scalars().all()
        return posts
    
@router.put('/updatepost/{post_id}')
async def update_post(
    post_id: UUID,  # match DB type
    post_in: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    print("id", post_id)

    # Get post by ID
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check ownership
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to update this post"
        )

    # Update post content
    post.content = post_in.content
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post

@router.delete('/deletepost/{post_id}')
async def delete_post(
    post_id = UUID,
    current_user : User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    
    if not post:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found!"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to delete the post"
        )
    
    await db.delete(post)
    await db.commit()
    return
    