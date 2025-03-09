from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

from app.core.config import settings
from app.core.logger import app_logger
from supabase import create_client

# SQLAlchemyのBaseクラス
Base = declarative_base()

# Supabaseクライアントの初期化
try:
    supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    app_logger.info("Supabaseクライアントの初期化に成功しました。")
except Exception as e:
    app_logger.error(f"Supabaseクライアントの初期化に失敗しました: {e}")
    supabase_client = None

# 同期SQLAlchemyエンジン
engine = create_engine(settings.DATABASE_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 非同期SQLAlchemyエンジン
async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    future=True,
)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 同期DBセッション取得用の依存性関数
def get_db() -> Generator:
    """
    DB接続のセッションを取得するための依存性関数
    
    Returns:
        Generator: DBセッションジェネレータ
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 非同期DBセッション取得用の依存性関数
async def get_async_db() -> AsyncSession:
    """
    非同期DB接続のセッションを取得するための依存性関数
    
    Returns:
        AsyncSession: 非同期DBセッション
    """
    async with AsyncSessionLocal() as session:
        yield session
