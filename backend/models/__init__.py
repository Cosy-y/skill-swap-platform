# importing all my data models 
from .user import UserCreate, UserUpdate, UserResponse, UserPublicResponse, Skill, Availability, UserRole
from .swap import SwapRequest, SwapResponse, SwapCreate, SwapUpdate, SwapStatus
from .review import ReviewCreate, ReviewResponse, ReviewUpdate
from .admin import AdminUserAction, PlatformMessage, PlatformMessageResponse, ReportData

# not sure if i need this __all__ thing but saw it in a tutorial
__all__ = [
    "UserCreate",
    "UserUpdate", 
    "UserResponse",
    "UserPublicResponse",
    "Skill",
    "Availability",
    "UserRole",
    "SwapRequest",
    "SwapResponse", 
    "SwapCreate",
    "SwapUpdate",
    "SwapStatus",
    "ReviewCreate",
    "ReviewResponse", 
    "ReviewUpdate",
    "AdminUserAction",
    "PlatformMessage",
    "PlatformMessageResponse",
    "ReportData"
]