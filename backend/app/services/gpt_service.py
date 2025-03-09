import openai
from typing import List, Dict, Any, Optional
from loguru import logger

from app.core.config import settings

# Configure OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


class GPTService:
    @staticmethod
    async def generate_post_variants(
        platform: str,
        title: str,
        keywords: List[str],
        num_variants: int = 2,
    ) -> List[str]:
        """
        Generate multiple post variant texts using GPT-4.
        
        Args:
            platform: The target platform (X, Reddit, ProductHunt)
            title: Main theme or title of the post
            keywords: List of keywords to include
            num_variants: Number of variants to generate (default: 2)
            
        Returns:
            List of generated post content variants
        """
        try:
            platform_context = {
                "x": "X (formerly Twitter) with max 280 chars, engaging, with hashtags",
                "reddit": "Reddit post targeting tech communities, informative, engaging, with a clear call to action",
                "producthunt": "Product Hunt launch post highlighting benefits, use cases, and uniqueness"
            }
            
            context = platform_context.get(platform.lower(), "social media")
            keywords_str = ", ".join(keywords)
            
            prompt = f"""Generate {num_variants} variations of a post for {context}.
            
            Post topic: {title}
            Keywords to include: {keywords_str}
            
            Each variation should:
            1. Be attention-grabbing and engaging
            2. Include relevant emojis where appropriate
            3. Use a conversational yet professional tone
            4. Include 2-3 relevant hashtags (for X)
            5. Be optimized for the specific platform
            6. Include a clear call to action
            
            Provide exactly {num_variants} different variations, each separated by [VARIANT].
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media marketer specializing in tech products."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            
            content = response.choices[0].message.content
            variants = content.split("[VARIANT]")
            
            # Clean up each variant
            cleaned_variants = [variant.strip() for variant in variants if variant.strip()]
            
            logger.info(f"Generated {len(cleaned_variants)} variants for platform: {platform}")
            
            return cleaned_variants
            
        except Exception as e:
            logger.error(f"Error generating GPT variants: {str(e)}")
            # Return basic fallback variants if API fails
            return [
                f"Check out our product: {title}. {' '.join(keywords[:3])} #tech",
                f"Excited to share {title}! Built with {' and '.join(keywords[:2])}. Feedback welcome! #dev"
            ]

gpt_service = GPTService()