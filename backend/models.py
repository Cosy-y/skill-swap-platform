from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class SwapStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"

class Skill(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: SkillLevel
    description: Optional[str] = Field(None, max_length=500)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    skills_offered: List[Skill] = []
    skills_wanted: List[Skill] = []
    availability: Dict[str, Any] = {}
    is_profile_public: bool = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    skills_offered: Optional[List[Skill]] = None
    skills_wanted: Optional[List[Skill]] = None
    availability: Optional[Dict[str, Any]] = None
    is_profile_public: Optional[bool] = None
    profile_image_url: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    location: Optional[str]
    bio: Optional[str]
    skills_offered: List[Skill]
    skills_wanted: List[Skill]
    availability: Dict[str, Any]
    is_profile_public: bool
    profile_image_url: Optional[str]
    rating: float
    total_swaps: int
    created_at: datetime
    updated_at: datetime

class UserPublicResponse(BaseModel):
    user_id: str
    full_name: str
    location: Optional[str]
    bio: Optional[str]
    skills_offered: List[Skill]
    skills_wanted: List[Skill]
    profile_image_url: Optional[str]
    rating: float
    total_swaps: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SwapRequest(BaseModel):
    requester_id: str
    target_user_id: str
    offered_skill: Skill
    requested_skill: Skill
    message: Optional[str] = Field(None, max_length=1000)
    proposed_duration: Optional[str] = None
    proposed_schedule: Optional[Dict[str, Any]] = None

class SwapResponse(BaseModel):
    swap_id: str
    requester_id: str
    target_user_id: str
    offered_skill: Skill
    requested_skill: Skill
    message: Optional[str]
    status: SwapStatus
    proposed_duration: Optional[str]
    proposed_schedule: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

class ReviewCreate(BaseModel):
    swap_id: str
    reviewer_id: str
    reviewee_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)

class ReviewResponse(BaseModel):
    review_id: str
    swap_id: str
    reviewer_id: str
    reviewer_name: str
    reviewee_id: str
    rating: int
    comment: Optional[str]
    created_at: datetime

class MessageCreate(BaseModel):
    swap_id: str
    sender_id: str
    content: str = Field(..., min_length=1, max_length=1000)

class MessageResponse(BaseModel):
    message_id: str
    swap_id: str
    sender_id: str
    sender_name: str
    content: str
    created_at: datetime
    is_read: bool

# Error response models
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

# Success response models
class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
