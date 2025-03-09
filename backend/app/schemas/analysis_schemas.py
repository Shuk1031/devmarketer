from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class VariantEngagement(BaseModel):
    variant_id: int
    likes: int
    comments: int
    shares: int
    upvotes: int


class PostEngagementAnalysis(BaseModel):
    post_id: int
    variants: List[VariantEngagement]


class EngagementFetchRequest(BaseModel):
    post_id: int


class EngagementFetchResponse(BaseModel):
    status: str
    updated_count: int