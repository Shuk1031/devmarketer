from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# パスワードハッシュのためのコンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: str, expires_delta: Optional[timedelta] = None, additional_data: Dict[str, Any] = {}
) -> str:
    """
    JWTアクセストークンを生成します。
    
    Args:
        subject: トークンのサブジェクト (通常はユーザーID)
        expires_delta: トークンの有効期限
        additional_data: トークンに追加する任意のデータ
        
    Returns:
        str: エンコードされたJWTトークン
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # JWTペイロードを作成
    to_encode = {"exp": expire, "sub": str(subject), **additional_data}
    
    # JWTトークンをエンコード
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """
    JWTトークンを検証します。
    
    Args:
        token: 検証するJWTトークン
        
    Returns:
        Dict[str, Any]: デコードされたトークンペイロード
    
    Raises:
        jwt.JWTError: トークンが無効な場合
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def verify_supabase_token(token: str) -> Dict[str, Any]:
    """
    SupabaseのJWTトークンを検証します。
    
    Args:
        token: 検証するSupabaseのJWTトークン
        
    Returns:
        Dict[str, Any]: デコードされたトークンペイロード
    
    Raises:
        jwt.JWTError: トークンが無効な場合
    """
    try:
        payload = jwt.decode(
            token, settings.SUPABASE_JWT_SECRET, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        return None