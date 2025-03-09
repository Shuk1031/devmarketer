# backend/app/services/auth_service.py
from sqlalchemy.orm import Session
from app.core.security import create_jwt_token, verify_jwt_token
from app.models.user import User as UserModel
from app.schemas.user_schemas import User
from app.db.session import SessionLocal

async def authenticate_user(supabase_token: str) -> User | None:
    """
    Supabase から受け取ったトークンを元にユーザーを認証する。
    本サンプルでは、トークンが "valid" の場合にユーザー情報を取得または新規作成し、Pydantic の User を返す。
    """
    if supabase_token != "valid":
        return None

    db: Session = SessionLocal()
    try:
        # 実際はトークンからメール等のユーザー情報を抽出して検索する
        user_obj = db.query(UserModel).filter(UserModel.email == "user@example.com").first()
        if not user_obj:
            user_obj = UserModel(email="user@example.com", name="Test User", auth_provider="supabase")
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
        return User.from_orm(user_obj)
    finally:
        db.close()

async def get_user_from_token(token: str) -> User | None:
    """
    JWT トークンを検証し、該当するユーザー情報をデータベースから取得する。
    """
    payload = verify_jwt_token(token)
    if payload is None:
        return None
    user_id = payload.get("user_id")
    db: Session = SessionLocal()
    try:
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_obj:
            return User.from_orm(user_obj)
        return None
    finally:
        db.close()