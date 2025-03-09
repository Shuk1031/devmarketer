import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import redis
from rq import Queue

from app.core.config import settings
from app.core.logger import app_logger

# Redis接続クライアント
try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL)
    app_logger.info("Redisクライアントの初期化に成功しました。")
    
    # RQ Queueの初期化
    schedule_queue = Queue(settings.REDIS_QUEUE_NAME, connection=redis_client)
    app_logger.info(f"Redisキュー '{settings.REDIS_QUEUE_NAME}' の初期化に成功しました。")
except Exception as e:
    app_logger.error(f"Redisクライアントの初期化に失敗しました: {e}")
    redis_client = None
    schedule_queue = None

class RedisScheduler:
    """Redisを使用したスケジュール管理クラス"""
    
    @staticmethod
    def schedule_job(
        post_id: int, 
        variant_id: int, 
        scheduled_at: datetime,
        platform: str,
        user_id: int
    ) -> str:
        """
        投稿ジョブをスケジュールします。
        
        Args:
            post_id: 投稿ID
            variant_id: 投稿バリアントID
            scheduled_at: スケジュール時間
            platform: 投稿先プラットフォーム
            user_id: ユーザーID
            
        Returns:
            str: スケジュールされたジョブのID
        """
        # ジョブデータを作成
        job_data = {
            "post_id": post_id,
            "variant_id": variant_id,
            "scheduled_at": scheduled_at.isoformat(),
            "platform": platform,
            "user_id": user_id,
            "status": "scheduled"
        }
        
        # ジョブをキューに追加
        # RQの遅延実行機能を使用
        job = schedule_queue.enqueue_at(
            scheduled_at,
            "app.tasks.scheduler.publish_post",
            job_data,
            result_ttl=86400  # 結果を24時間保持
        )
        
        app_logger.info(f"ジョブをスケジュールしました: {job.id}, 実行時間: {scheduled_at}")
        return job.id
    
    @staticmethod
    def cancel_job(job_id: str) -> bool:
        """
        スケジュールされたジョブをキャンセルします。
        
        Args:
            job_id: キャンセルするジョブのID
            
        Returns:
            bool: キャンセルに成功したかどうか
        """
        try:
            # ジョブを取得して削除
            job = schedule_queue.fetch_job(job_id)
            if job:
                job.cancel()
                app_logger.info(f"ジョブをキャンセルしました: {job_id}")
                return True
            app_logger.warning(f"ジョブが見つかりませんでした: {job_id}")
            return False
        except Exception as e:
            app_logger.error(f"ジョブのキャンセルに失敗しました: {e}")
            return False
    
    @staticmethod
    def get_all_jobs() -> List[Dict[str, Any]]:
        """
        すべてのスケジュールされたジョブを取得します。
        
        Returns:
            List[Dict[str, Any]]: スケジュールされたジョブのリスト
        """
        try:
            # キュー内のすべてのジョブを取得
            job_ids = schedule_queue.get_job_ids()
            jobs = []
            
            for job_id in job_ids:
                job = schedule_queue.fetch_job(job_id)
                if job and not job.is_finished:
                    # ジョブがまだ終了していなければリストに追加
                    job_data = job.args[0] if job.args else {}
                    jobs.append({
                        "job_id": job.id,
                        "post_id": job_data.get("post_id"),
                        "variant_id": job_data.get("variant_id"),
                        "scheduled_at": job_data.get("scheduled_at"),
                        "platform": job_data.get("platform"),
                        "user_id": job_data.get("user_id"),
                        "status": job_data.get("status")
                    })
            
            return jobs
        except Exception as e:
            app_logger.error(f"ジョブの取得に失敗しました: {e}")
            return []
    
    @staticmethod
    def get_job(job_id: str) -> Optional[Dict[str, Any]]:
        """
        指定されたIDのジョブを取得します。
        
        Args:
            job_id: 取得するジョブのID
            
        Returns:
            Optional[Dict[str, Any]]: ジョブデータ、存在しない場合はNone
        """
        try:
            job = schedule_queue.fetch_job(job_id)
            if job:
                job_data = job.args[0] if job.args else {}
                return {
                    "job_id": job.id,
                    "post_id": job_data.get("post_id"),
                    "variant_id": job_data.get("variant_id"),
                    "scheduled_at": job_data.get("scheduled_at"),
                    "platform": job_data.get("platform"),
                    "user_id": job_data.get("user_id"),
                    "status": job_data.get("status"),
                    "result": job.result,
                    "is_finished": job.is_finished,
                    "is_failed": job.is_failed
                }
            return None
        except Exception as e:
            app_logger.error(f"ジョブの取得に失敗しました: {e}")
            return None
