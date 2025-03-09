# backend/app/api/endpoints/schedule.py
from fastapi import APIRouter, HTTPException, Depends, Query, status, Body
from typing import Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schedule_schemas import JobResponse, BulkJobIds, JobDetail, RecurringScheduleCreate
from app.services.schedule_service import (
    get_schedule_jobs,
    get_job_detail,
    cancel_job,
    bulk_cancel_jobs,
    create_recurring_schedule,
    pause_all_jobs,
    resume_jobs
)
from app.services.auth_service import get_current_user
from app.schemas.user_schemas import User

router = APIRouter()

@router.get("/jobs", response_model=List[JobResponse])
async def list_schedule_jobs(
    platform: Optional[str] = Query(None, description="特定プラットフォームのジョブのみ取得"),
    status: Optional[str] = Query(None, description="特定ステータス(pending/running/completed)のジョブのみ取得"),
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="オフセット"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    スケジュールされた投稿ジョブの一覧を取得します。
    
    Args:
        platform: フィルタリングするプラットフォーム（省略可）
        status: フィルタリングするステータス（省略可）
        limit: 取得件数
        offset: オフセット位置
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        List[JobResponse]: ジョブ一覧
    """
    try:
        jobs = await get_schedule_jobs(
            user_id=current_user.id,
            platform=platform,
            status=status,
            limit=limit,
            offset=offset,
            db=db
        )
        return jobs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"スケジュールジョブ取得中にエラーが発生しました: {str(e)}"
        )

@router.get("/jobs/{job_id}", response_model=JobDetail)
async def get_job_details(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    特定のスケジュールジョブの詳細情報を取得します。
    
    Args:
        job_id: ジョブID
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        JobDetail: ジョブ詳細情報
    """
    try:
        job_detail = await get_job_detail(job_id, user_id=current_user.id, db=db)
        if not job_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ジョブID {job_id} が見つかりません"
            )
        return job_detail
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ジョブ詳細取得中にエラーが発生しました: {str(e)}"
        )

@router.delete("/jobs/{job_id}", response_model=dict)
async def cancel_schedule_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    指定したスケジュールジョブをキャンセルします。
    
    Args:
        job_id: キャンセルするジョブID
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: キャンセル状態
    """
    try:
        result = await cancel_job(job_id, user_id=current_user.id, db=db)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ジョブキャンセル中にエラーが発生しました: {str(e)}"
        )

@router.post("/jobs/bulk-cancel", response_model=dict)
async def bulk_cancel_schedule_jobs(
    job_ids: BulkJobIds,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    複数のスケジュールジョブを一括でキャンセルします。
    
    Args:
        job_ids: キャンセルするジョブIDリスト
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: キャンセル状態とキャンセル成功/失敗したIDのリスト
    """
    try:
        result = await bulk_cancel_jobs(job_ids.ids, user_id=current_user.id, db=db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ジョブ一括キャンセル中にエラーが発生しました: {str(e)}"
        )

@router.post("/recurring", response_model=dict)
async def create_recurring_schedule_endpoint(
    schedule: RecurringScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    定期的な投稿スケジュールを作成します。
    
    Args:
        schedule: 定期スケジュール設定
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: スケジュール作成状態
    """
    try:
        result = await create_recurring_schedule(
            user_id=current_user.id,
            post_id=schedule.post_id,
            variant_id=schedule.variant_id,
            recurrence_pattern=schedule.recurrence_pattern,
            recurrence_days=schedule.recurrence_days,
            start_time=schedule.start_time,
            end_date=schedule.end_date,
            db=db
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"定期スケジュール作成中にエラーが発生しました: {str(e)}"
        )

@router.post("/pause-all", response_model=dict)
async def pause_all_jobs_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    ユーザーのすべてのスケジュールジョブを一時停止します。
    
    Args:
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: 停止状態
    """
    try:
        result = await pause_all_jobs(user_id=current_user.id, db=db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ジョブ一時停止中にエラーが発生しました: {str(e)}"
        )

@router.post("/resume", response_model=dict)
async def resume_jobs_endpoint(
    job_ids: BulkJobIds = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    一時停止したジョブを再開します。
    
    Args:
        job_ids: 再開するジョブIDリスト
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: 再開状態
    """
    try:
        result = await resume_jobs(job_ids.ids, user_id=current_user.id, db=db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ジョブ再開中にエラーが発生しました: {str(e)}"
        )
