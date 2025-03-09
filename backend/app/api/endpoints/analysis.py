# backend/app/api/endpoints/analysis.py
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analysis_schemas import (
    EngagementResponse, 
    EngagementFetchRequest, 
    EngagementSummary,
    PerformanceMetrics
)
from app.services.analysis_service import (
    get_engagements, 
    fetch_latest_engagements,
    get_performance_metrics,
    get_best_performing_variant
)
from app.services.auth_service import get_current_user
from app.schemas.user_schemas import User

router = APIRouter()

@router.get("/engagements", response_model=EngagementResponse)
async def get_post_engagements(
    post_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    指定した投稿のエンゲージメント結果を取得します。
    
    Args:
        post_id: 投稿ID
        start_date: フィルタリング開始日時（省略可）
        end_date: フィルタリング終了日時（省略可）
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        EngagementResponse: エンゲージメント情報
    """
    try:
        # 投稿の所有者確認を追加すべき
        data = await get_engagements(
            post_id,
            user_id=current_user.id,
            db=db,
            start_date=start_date,
            end_date=end_date
        )
        return data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"エンゲージメント取得中にエラーが発生しました: {str(e)}"
        )

@router.post("/fetch-latest", response_model=dict)
async def fetch_latest_engagements_endpoint(
    request: EngagementFetchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    最新のエンゲージメントデータをSNS APIから取得してDBに保存します。
    
    Args:
        request: 取得対象の投稿ID
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: 更新状態
    """
    try:
        # 投稿の所有者確認を追加すべき
        result = await fetch_latest_engagements(
            request.post_id,
            user_id=current_user.id,
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
            detail=f"エンゲージメント取得中にエラーが発生しました: {str(e)}"
        )

@router.get("/performance", response_model=PerformanceMetrics)
async def get_performance_metrics_endpoint(
    platform: Optional[str] = Query(None, description="フィルタリングするプラットフォーム"),
    days: int = Query(30, description="過去何日分のデータを取得するか", ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    ユーザーの投稿パフォーマンス全体を分析したメトリクスを提供します。
    
    Args:
        platform: 特定プラットフォームでフィルタリング（省略可）
        days: 取得期間（日数）
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        PerformanceMetrics: パフォーマンス統計情報
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = await get_performance_metrics(
            user_id=current_user.id,
            platform=platform,
            start_date=start_date,
            end_date=end_date,
            db=db
        )
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"パフォーマンスメトリクス取得中にエラーが発生しました: {str(e)}"
        )

@router.get("/best-variant/{post_id}", response_model=dict)
async def get_best_variant(
    post_id: int,
    metric: str = Query("engagement_rate", description="最適化基準となるメトリック"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    指定投稿の最も効果の高いバリエーションを特定します。
    
    Args:
        post_id: 投稿ID
        metric: 評価基準（likes, comments, shares, engagement_rate など）
        current_user: 認証済みユーザー
        db: データベースセッション
        
    Returns:
        dict: 最適バリエーション情報
    """
    try:
        # 投稿の所有者確認を追加すべき
        result = await get_best_performing_variant(
            post_id,
            metric=metric,
            user_id=current_user.id,
            db=db
        )
        return {
            "best_variant_id": result.variant_id,
            "content": result.content,
            "metric_value": result.metric_value,
            "improvement_percentage": result.improvement_percentage  # 平均と比較した改善率
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"最適バリエーション取得中にエラーが発生しました: {str(e)}"
        )
