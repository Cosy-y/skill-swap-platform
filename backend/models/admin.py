from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# admin actions for users
class AdminUserAction(BaseModel):
    user_id: str
    action: str  # "ban", "unban", "approve_skill", "reject_skill"
    reason: Optional[str] = None

# platform message from admin
class PlatformMessage(BaseModel):
    title: str
    content: str
    message_type: str = "info"  # "info", "warning", "maintenance"
    
class PlatformMessageResponse(BaseModel):
    id: str
    title: str
    content: str
    message_type: str
    created_at: datetime
    created_by: str  # admin user id

# report data for admins
class ReportData(BaseModel):
    total_users: int
    total_swaps: int
    pending_swaps: int
    completed_swaps: int
    average_rating: float
    recent_activity: List[dict]
