from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# review/rating for completed swaps
class ReviewCreate(BaseModel):
    swap_id: str
    reviewee_id: str  # person being reviewed
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: Optional[str] = None
    
class ReviewResponse(BaseModel):
    id: str
    swap_id: str
    reviewer_id: str  # person who wrote the review
    reviewee_id: str  # person being reviewed
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    
class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
