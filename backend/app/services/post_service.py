from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from loguru import logger

from app.core.config import settings
from app.models.post import Post, Platform, PostStatus
from app.models.post_variant import PostVariant
from app.services.gpt_service import gpt_service


class PostService:
    @staticmethod
    async def create_post_with_variants(
        db: AsyncSession,
        user_id: int,
        platform: Platform,
        title: str,
        keywords: List[str],
    ) -> Dict[str, Any]:
        """
        Create a new post and generate variants with GPT.
        
        Args:
            db: Database session
            user_id: User ID creating the post
            platform: Target platform (X, Reddit, ProductHunt)
            title: Post title/theme
            keywords: List of keywords for the post
            
        Returns:
            Dictionary with post data and generated variants
        """
        # Create a new post
        post = Post(
            user_id=user_id,
            platform=platform,
            status=PostStatus.DRAFT
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        
        # Generate variants with GPT
        variant_texts = await gpt_service.generate_post_variants(
            platform=platform.value,
            title=title,
            keywords=keywords
        )
        
        # Create variant objects
        variants = []
        for content in variant_texts:
            variant = PostVariant(
                post_id=post.id,
                content=content
            )
            db.add(variant)
            variants.append(variant)
        
        await db.commit()
        
        # Refresh variants to get their IDs
        for variant in variants:
            await db.refresh(variant)
        
        return {
            "post_id": post.id,
            "platform": platform.value,
            "variants": [
                {"id": variant.id, "content": variant.content}
                for variant in variants
            ]
        }
    
    @staticmethod
    async def publish_post(
        db: AsyncSession,
        post_id: int,
        variant_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Publish a post immediately to the target platform.
        
        Args:
            db: Database session
            post_id: Post ID to publish
            variant_id: Specific variant to publish (optional)
            
        Returns:
            Status and response from the social network
        """
        # Get post
        stmt = select(Post).where(Post.id == post_id)
        result = await db.execute(stmt)
        post = result.scalar_one_or_none()
        
        if not post:
            raise ValueError(f"Post with ID {post_id} not found")
        
        # If variant not specified, get the first one
        if variant_id is None:
            stmt = select(PostVariant).where(PostVariant.post_id == post_id)
            result = await db.execute(stmt)
            variant = result.scalar_one_or_none()
            
            if not variant:
                raise ValueError(f"No variants found for post ID {post_id}")
                
            variant_id = variant.id
        else:
            # Get the specified variant
            stmt = select(PostVariant).where(
                PostVariant.id == variant_id,
                PostVariant.post_id == post_id
            )
            result = await db.execute(stmt)
            variant = result.scalar_one_or_none()
            
            if not variant:
                raise ValueError(f"Variant ID {variant_id} not found for post ID {post_id}")
        
        # Now we have the post and variant, publish to the respective platform
        platform = post.platform
        content = variant.content
        
        # Placeholder for actual API calls to social platforms
        sns_response = await PostService._publish_to_platform(platform, content)
        
        # Update post status
        post.status = PostStatus.PUBLISHED
        await db.commit()
        
        return {
            "status": "published",
            "sns_response": sns_response
        }
    
    @staticmethod
    async def _publish_to_platform(platform: Platform, content: str) -> Dict[str, Any]:
        """
        Publish content to the selected social media platform.
        
        Args:
            platform: Target platform
            content: Content to publish
            
        Returns:
            Response from the platform API
        """
        try:
            if platform == Platform.X:
                return await PostService._publish_to_twitter(content)
            elif platform == Platform.REDDIT:
                return await PostService._publish_to_reddit(content)
            elif platform == Platform.PRODUCTHUNT:
                return await PostService._publish_to_producthunt(content)
            else:
                return {"error": "Unsupported platform"}
        except Exception as e:
            logger.error(f"Error publishing to {platform}: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    async def _publish_to_twitter(content: str) -> Dict[str, Any]:
        """
        Publish to Twitter/X using their API.
        
        In the real implementation, use the Twitter API v2 with proper authentication.
        This is a placeholder implementation.
        """
        try:
            # TODO: Implement actual Twitter API call
            # Using httpx as an example
            api_key = settings.TWITTER_API_KEY
            api_secret = settings.TWITTER_API_SECRET
            access_token = settings.TWITTER_ACCESS_TOKEN
            access_secret = settings.TWITTER_ACCESS_SECRET
            
            # Placeholder for authentication and API call
            # In a real implementation, use tweepy or the Twitter API directly
            
            logger.info(f"Published to Twitter: {content[:50]}...")
            return {"id": "12345678", "text": content, "platform": "twitter"}
        except Exception as e:
            logger.error(f"Twitter API error: {str(e)}")
            raise
    
    @staticmethod
    async def _publish_to_reddit(content: str) -> Dict[str, Any]:
        """Publish to Reddit (placeholder)"""
        # TODO: Implement actual Reddit API call
        return {"id": "abc123", "text": content, "platform": "reddit"}
    
    @staticmethod
    async def _publish_to_producthunt(content: str) -> Dict[str, Any]:
        """Publish to Product Hunt (placeholder)"""
        # TODO: Implement actual Product Hunt API call
        return {"id": "ph12345", "text": content, "platform": "producthunt"}
    
    @staticmethod
    async def get_post_with_variants(
        db: AsyncSession,
        post_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get a post with all its variants.
        
        Args:
            db: Database session
            post_id: Post ID to retrieve
            
        Returns:
            Post data with variants or None if not found
        """
        stmt = select(Post).where(Post.id == post_id)
        result = await db.execute(stmt)
        post = result.scalar_one_or_none()
        
        if not post:
            return None
        
        # Get variants
        stmt = select(PostVariant).where(PostVariant.post_id == post_id)
        result = await db.execute(stmt)
        variants = result.scalars().all()
        
        return {
            "id": post.id,
            "user_id": post.user_id,
            "platform": post.platform.value,
            "status": post.status.value,
            "scheduled_at": post.scheduled_at,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "variants": [
                {
                    "id": variant.id,
                    "content": variant.content,
                    "created_at": variant.created_at
                }
                for variant in variants
            ]
        }


post_service = PostService()