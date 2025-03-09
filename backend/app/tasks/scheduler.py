# backend/app/tasks/scheduler.py
import json
import asyncio
from app.db.redis_client import redis_client
from app.services.post_service import publish_post
from app.core.logger import logger

async def scheduler_loop():
    """
    Redis キュー "schedule_queue" からジョブをポーリングし、
    所定の投稿（post_id）を実行するバックグラウンドワーカー
    """
    while True:
        job_data = redis_client.lpop("schedule_queue")
        if job_data:
            try:
                job = json.loads(job_data)
                logger.info(f"Executing scheduled job: {job}")
                post_id = job.get("post_id")
                if post_id is not None:
                    # 即時投稿の実行（SNS API 連携等の実装は post_service.publish_post 内で処理）
                    result = await publish_post(post_id)
                    logger.info(f"Post ID {post_id} published with result: {result}")
                else:
                    logger.error("Job does not contain post_id")
            except Exception as e:
                logger.error(f"Error processing job: {e}")
        else:
            # キューにジョブが無い場合は少し待機
            await asyncio.sleep(5)

if __name__ == "__main__":
    # asyncio.run() で scheduler_loop を実行
    asyncio.run(scheduler_loop())