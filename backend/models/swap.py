from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# different states a swap can be in
class SwapStatus(str, Enum):
    PENDING = "pending"        # waiting for response
    ACCEPTED = "accepted"      # they said yes
    IN_PROGRESS = "in_progress"  # currently learning/teaching
    COMPLETED = "completed"    # all done
    CANCELLED = "cancelled"    # someone cancelled
    REJECTED = "rejected"      # they said no

# basic swap request data
class SwapRequest(BaseModel):
    requester_id: str
    requestee_id: str
    requester_skill: str  # what the person asking can teach
    requested_skill: str  # what they want to learn
    message: Optional[str] = None  # optional message
    status: SwapStatus = SwapStatus.PENDING
    created_at: datetime
    updated_at: datetime

# full swap response with id
class SwapResponse(BaseModel):
    id: str
    requester_id: str  # person who asked
    requestee_id: str  # person being asked
    requester_skill: str
    requested_skill: str
    message: Optional[str] = None
    status: SwapStatus
    created_at: datetime
    updated_at: datetime
    
# for creating new swap requests
class SwapCreate(BaseModel):
    requestee_id: str  # who you want to swap with
    requester_skill: str  # what you're offering
    requested_skill: str  # what you want
    message: Optional[str] = None

class SwapUpdate(BaseModel):
    status: SwapStatus
    message: Optional[str] = None
