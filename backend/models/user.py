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
    name: str
    email: EmailStr
    location: Optional[str] = None  # city, state
    bio: Optional[str] = None
    skills_offered: List[Skill] = []  # skills they can teach
    skills_wanted: List[Skill] = []   # skills they want to learn
    availability: Optional[Availability] = None
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
    id: str
    name: str
    email: str
    location: Optional[str] = None
    bio: Optional[str] = None
    skills_offered: List[Skill] = []
    skills_wanted: List[Skill] = []
    availability: Optional[Availability] = None
    is_profile_public: bool = True
    profile_photo_url: Optional[str] = None
    rating: Optional[float] = None  # user rating from swaps
    total_swaps: int = 0  # how many swaps they've done
    role: UserRole = UserRole.USER
    is_banned: bool = False
    created_at: datetime
    updated_at: datetime

# what other users can see (public profile)
class UserPublicResponse(BaseModel):
    id: str
    name: str
    location: Optional[str] = None
    bio: Optional[str] = None
    skills_offered: List[Skill] = []
    skills_wanted: List[Skill] = []
    availability: Optional[Availability] = None
    rating: Optional[float] = None
    total_swaps: int = 0
