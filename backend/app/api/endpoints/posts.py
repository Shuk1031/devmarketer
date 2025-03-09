# backend/app/api/endpoints/posts.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Any
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.post_schemas import PostCreate, PostResponse, ScheduleRequest
from app.services.post_service import create_post_with_variants, schedule_post, publish_post
from app.services.auth_service import get_current_user
from app.schemas.user_schemas import User

router = APIRouter()

@router.post("/create", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    新規投稿を作成し、GPT-4で複数の文案バリエーションを生成します。
    
    Args:
        post: プラットフォーム、タイトル、キーワードなどの投稿情報
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        PostResponse: 作成された投稿ID、バリエーション一覧
    """
    try:
        result = await create_post_with_variants(post, user_id=current_user.id, db=db)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"投稿作成中にエラーが発生しました: {str(e)}",
        )

@router.post("/schedule/{post_id}", response_model=dict)
async def schedule_post_endpoint(
    post_id: int, 
    schedule_request: ScheduleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    投稿をスケジュールします。
    
    Args:
        post_id: スケジュールする投稿ID
        schedule_request: スケジュール日時とバリエーションID
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: スケジュール状態とジョブID
    """
    try:
        # 投稿の所有者確認を追加すべき
        result = await schedule_post(
            post_id, 
            schedule_request.variant_id, 
            schedule_request.scheduled_at,
            user_id=current_user.id,
            db=db
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except HTTPException:
        # 既に HTTPException の場合はそのまま再送
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"スケジュール設定中にエラーが発生しました: {str(e)}",
        )

@router.post("/publish/{post_id}", response_model=dict)
async def publish_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    投稿を即時公開します。
    
    Args:
        post_id: 公開する投稿ID
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: 公開状態とSNSレスポンス
    """
    try:
        # 投稿の所有者確認を追加すべき
        result = await publish_post(post_id, user_id=current_user.id, db=db)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"投稿公開中にエラーが発生しました: {str(e)}",
        )
