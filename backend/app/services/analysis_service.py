# backend/app/services/analysis_service.py
import random
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.engagement import Engagement
from app.models.post_variant import PostVariant
from app.models.post import Post

async def get_engagements(post_id: int) -> dict:
    """
    指定投稿の各バリエーションについて、DB 内のエンゲージメントデータ（likes, comments, shares, upvotes）を集計して返す。
    """
    db: Session = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return {"error": "Post not found"}
        
        variants = db.query(PostVariant).filter(PostVariant.post_id == post_id).all()
        result = {"post_id": post_id, "variants": []}
        for variant in variants:
            engagement = db.query(Engagement).filter(Engagement.post_variant_id == variant.id).first()
            if engagement:
                result["variants"].append({
                    "variant_id": variant.id,
                    "likes": engagement.likes,
                    "comments": engagement.comments,
                    "shares": engagement.shares,
                    "upvotes": engagement.upvotes
                })
            else:
                result["variants"].append({
                    "variant_id": variant.id,
                    "likes": 0,
                    "comments": 0,
                    "shares": 0,
                    "upvotes": 0
                })
    finally:
        db.close()
    return result

async def fetch_latest_engagements(post_id: int) -> dict:
    """
    SNS API から最新のエンゲージメントデータを（ダミー値として）取得し、DB のエンゲージメントレコードを更新する。
    ※実際の実装では、外部 API との連携により動的な値を取得する。
    """
    db: Session = SessionLocal()
    try:
        variant = db.query(PostVariant).filter(PostVariant.post_id == post_id).first()
        if not variant:
            return {"error": "No variants found for post"}
        
        # ダミーのエンゲージメント数（ランダム値を生成）
        likes = random.randint(0, 100)
        comments = random.randint(0, 50)
        shares = random.randint(0, 20)
        upvotes = random.randint(0, 100)
        
        engagement = db.query(Engagement).filter(Engagement.post_variant_id == variant.id).first()
        if not engagement:
            from app.models.engagement import Engagement
            engagement = Engagement(
                post_variant_id=variant.id,
                likes=likes,
                comments=comments,
                shares=shares,
                upvotes=upvotes
            )
            db.add(engagement)
        else:
            engagement.likes = likes
            engagement.comments = comments
            engagement.shares = shares
            engagement.upvotes = upvotes
        db.commit()
    finally:
        db.close()
    return {"status": "success", "updated_count": 1}