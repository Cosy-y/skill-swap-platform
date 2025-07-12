# importing all my data models 
from .user import UserCreate, UserUpdate, UserResponse, UserPublicResponse, Skill, Availability, UserRole, LoginRequest, SuccessResponse
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
    "LoginRequest",
    "SuccessResponse",
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