# backend/app/api/endpoints/auth.py
from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
import logging

from app.core.config import settings
from app.core.security import create_access_token, verify_supabase_token, get_password_hash
from app.db.session import get_db
from app.services.auth_service import get_current_user, authenticate_user, check_rate_limit
from app.schemas.user_schemas import Token, TokenPayload, User, UserCreate

# ロギング設定
logger = logging.getLogger(__name__)

# OAuthスキーム（トークン取得用）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
) -> Any:
    """
    Supabase認証トークンを使用してログインします。
    
    Args:
        request: リクエスト情報（レート制限に使用）
        token: SupabaseのOAuthトークン
        db: データベースセッション
        
    Returns:
        Token: アクセストークン情報
    """
    # レート制限チェック（ブルートフォース攻撃対策）
    client_ip = request.client.host
    if not check_rate_limit(client_ip, "login"):
        logger.warning(f"レート制限超過: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="リクエスト数が多すぎます。しばらく待ってから再試行してください。",
        )
    
    try:
        # Supabaseトークンを検証
        payload = verify_supabase_token(token)
        
        # ペイロードからユーザー情報を取得
        user_email = payload.get("email")
        auth_provider = payload.get("provider", "email")
        user_name = payload.get("name", "")
        
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="トークンから有効なユーザー情報を取得できません",
            )
        
        # ユーザーをDBに登録または取得
        user = authenticate_user(db, user_email, auth_provider, name=user_name)
        
        # JWTトークンを生成
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.id), 
            expires_delta=access_token_expires,
            additional_data={"email": user.email, "name": user.name}
        )
        
        # 監査ログ
        logger.info(f"ユーザーログイン成功: {user_email}, provider: {auth_provider}")
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except JWTError as e:
        logger.error(f"JWT検証エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なSupabaseトークンです",
        )
    except Exception as e:
        logger.error(f"ログインエラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ログイン処理中にエラーが発生しました",
        )

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    現在ログインしているユーザーの情報を取得します。
    
    Args:
        current_user: 現在のユーザー（依存性注入による）
        
    Returns:
        User: ユーザー情報
    """
    return current_user

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    ユーザーをログアウトします。
    
    注: JWTベースの認証では実際のログアウトはクライアント側で行われます。
    このエンドポイントは監査目的で提供されています。
    
    Args:
        current_user: 現在のユーザー
        
    Returns:
        dict: ログアウト状態
    """
    # 監査ログ
    logger.info(f"ユーザーログアウト: {current_user.email}")
    
    # フロントエンドでJWTトークンを削除する指示を返す
    return {"status": "success", "message": "ログアウトしました"}
