from fastapi import FastAPI

from app.api.v1.endpoints import auth, posts

app = FastAPI(
    title="Next Social Media app",
    description="Backend for nexa",
    version="0.1.0"
)

app.include_router(auth.router, prefix="/auth", tags=['Auth'])
app.include_router(posts.router, prefix="/post", tags=["Poss"])
@app.get('/')
async def root():
    return {
        "message":"This is nexa app APIs"
    }
    