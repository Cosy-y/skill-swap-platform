from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

# user types 
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

# skill model - represents a skill someone has
class Skill(BaseModel):
    name: str
    description: Optional[str] = None
    proficiency_level: str  # beginner, intermediate, advanced

# availability model - when they can do skill swaps
class Availability(BaseModel):
    days: List[str]  # monday, tuesday etc
    time_slots: List[str]  # morning, afternoon, evening
    timezone: Optional[str] = "UTC"

# model for creating new users (signup form data)
class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Added password field for registration
    full_name: str  # Changed from 'name' to 'full_name' to match auth.py
    location: Optional[str] = None  # city, state
    bio: Optional[str] = None
    skills_offered: List[Skill] = []  # skills they can teach
    skills_wanted: List[Skill] = []   # skills they want to learn
    availability: Optional[dict] = None  # Changed to dict to match auth.py
    is_profile_public: bool = True  # public by default

# for updating existing users
class UserUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills_offered: Optional[List[Skill]] = None
    skills_wanted: Optional[List[Skill]] = None
    availability: Optional[Availability] = None
    is_profile_public: Optional[bool] = None
    profile_photo_url: Optional[str] = None  # maybe add profile pics later

# full user data response
class UserResponse(BaseModel):
    user_id: str  # Changed from 'id' to 'user_id'
    email: str
    full_name: str  # Changed from 'name' to 'full_name'
    location: Optional[str] = None
    bio: Optional[str] = None
    skills_offered: List[Skill] = []
    skills_wanted: List[Skill] = []
    availability: Optional[dict] = None  # Changed to dict
    is_profile_public: bool = True
    profile_image_url: Optional[str] = None  # Changed from 'profile_photo_url'
    rating: float = 0.0  # Default to 0.0 instead of Optional
    total_swaps: int = 0  # how many swaps they've done
    role: UserRole = UserRole.USER
    is_banned: bool = False
    ban_reason: Optional[str] = None
    banned_at: Optional[datetime] = None
    banned_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# what other users can see (public profile)
class UserPublicResponse(BaseModel):
    user_id: str  # Changed from 'id' to match database
    full_name: str  # Changed from 'name' to match database
    location: Optional[str] = None
    bio: Optional[str] = None
    skills_offered: List[Skill] = []
    skills_wanted: List[Skill] = []
    availability: Optional[dict] = None  # Changed to dict to match database
    rating: float = 0.0  # Changed to default 0.0
    total_swaps: int = 0

# Authentication models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None
