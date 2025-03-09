from fastapi import APIRouter
from app.api.endpoints import auth, posts, schedule, analysis

# メインAPIルーター
api_router = APIRouter()

# 各エンドポイントモジュールをルーターに登録
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
