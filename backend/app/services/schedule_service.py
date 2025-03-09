from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from loguru import logger

from app.db.redis_client import redis_client, schedule_queue
from app.models.post import Post, PostStatus
from app.models.post_variant import PostVariant
from app.services.post_service import post_service


class ScheduleService:
    @staticmethod
    async def schedule_post(
        db: AsyncSession,
        post_id: int,
        variant_id: int,
        scheduled_at: datetime
    ) -> Dict[str, Any]:
        """
        Schedule a post for future publication.
        
        Args:
            db: Database session
            post_id: Post ID to schedule
            variant_id: Variant ID to publish
            scheduled_at: When to publish the post
            
        Returns:
            Scheduling status and job ID
        """
        # Verify post exists
        stmt = select(Post).where(Post.id == post_id)
        result = await db.execute(stmt)
        post = result.scalar_one_or_none()
        
        if not post:
            raise ValueError(f"Post with ID {post_id} not found")
        
        # Verify variant exists
        stmt = select(PostVariant).where(
            PostVariant.id == variant_id,
            PostVariant.post_id == post_id
        )
        result = await db.execute(stmt)
        variant = result.scalar_one_or_none()
        
        if not variant:
            raise ValueError(f"Variant ID {variant_id} not found for post ID {post_id}")
        
        # Update post scheduled time and status
        post.scheduled_at = scheduled_at
        post.status = PostStatus.SCHEDULED
        await db.commit()
        
        # Create job in Redis queue
        job_data = {
            "post_id": post_id,
            "variant_id": variant_id,
            "platform": post.platform.value,
            "scheduled_at": scheduled_at.isoformat()
        }
        
        # Calculate time difference for scheduling
        time_diff = scheduled_at - datetime.utcnow()
        seconds_until_publish = int(time_diff.total_seconds())
        
        if seconds_until_publish <= 0:
            # If scheduled time is in the past or now, publish immediately
            publish_result = await post_service.publish_post(db, post_id, variant_id)
            return {
                "status": "published_immediately",
                "job_id": "immediate",
                "result": publish_result
            }
        
        # Schedule job with RQ
        job_id = f"post:{post_id}:variant:{variant_id}"
        job = schedule_queue.enqueue_in(
            time_delta=time_diff,
            func="app.tasks.scheduler.publish_scheduled_post",
            post_id=post_id,
            variant_id=variant_id,
            job_id=job_id
        )
        
        # Store additional metadata in Redis
        redis_key = f"schedule:post:{post_id}"
        await redis_client.set(redis_key, json.dumps(job_data))
        
        return {
            "status": "scheduled",
            "job_id": job_id,
            "scheduled_at": scheduled_at.isoformat()
        }
    
    @staticmethod
    async def get_schedule_jobs() -> list:
        """
        Redis キュー "schedule_queue" からすべてのジョブを取得してリストで返す。
        """
        jobs = []
        job_list = redis_client.lrange("schedule_queue", 0, -1)
        for job_data in job_list:
            try:
                job = json.loads(job_data)
                jobs.append(job)
            except Exception:
                continue
        return jobs

    @staticmethod
    async def cancel_job(job_id: str) -> dict:
        """
        指定された job_id のジョブを Redis キューから削除し、キャンセル処理を行う。
        """
        job_list = redis_client.lrange("schedule_queue", 0, -1)
        for job_data in job_list:
            try:
                job = json.loads(job_data)
                if job.get("job_id") == job_id:
                    redis_client.lrem("schedule_queue", 1, job_data)
                    return {"status": "cancelled"}
            except Exception:
                continue
        return {"status": "job not found"}