from fastapi import APIRouter, HTTPException, Depends, Query
from firebase_init import db
from models.admin import AdminUserAction, PlatformMessage, PlatformMessageResponse, ReportData, AdminStats
from models.user import UserRole
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/admin", tags=["Admin"])

def check_db_connection():
    # make sure firebase is working
    if db is None:
        raise HTTPException(
            status_code=500, 
            detail="Database connection not available. Please check Firebase configuration."
        )

def check_admin_role(user_id: str):
    # verify user is admin
    check_db_connection()
    user_doc = db.collection("users").document(user_id).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user_doc.to_dict()
    if user_data.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user_data

@router.post("/user-action")
def admin_user_action(action: AdminUserAction, admin_id: str):
    # perform admin actions on users
    check_admin_role(admin_id)
    try:
        user_doc = db.collection("users").document(action.user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Target user not found")
        
        if action.action == "ban":
            db.collection("users").document(action.user_id).update({
                "is_banned": True,
                "ban_reason": action.reason,
                "banned_at": datetime.utcnow(),
                "banned_by": admin_id
            })
        elif action.action == "unban":
            db.collection("users").document(action.user_id).update({
                "is_banned": False,
                "ban_reason": None,
                "banned_at": None,
                "banned_by": None
            })
        elif action.action == "approve_skill":
            # logic to approve a skill
            pass
        elif action.action == "reject_skill":
            # logic to reject a skill
            pass
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        return {"message": f"Action '{action.action}' performed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error performing action: {str(e)}")

@router.get("/swaps")
def get_all_swaps(admin_id: str, status: Optional[str] = None, limit: int = 100):
    # get all swaps for monitoring
    check_admin_role(admin_id)
    try:
        query = db.collection("swaps")
        if status:
            query = query.where("status", "==", status)
        
        swaps = query.limit(limit).stream()
        return [swap.to_dict() for swap in swaps]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching swaps: {str(e)}")

@router.post("/message", response_model=PlatformMessageResponse)
def send_platform_message(message: PlatformMessage, admin_id: str):
    # send platform-wide message
    check_admin_role(admin_id)
    try:
        message_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        message_dict = {
            "id": message_id,
            "title": message.title,
            "content": message.content,
            "message_type": message.message_type,
            "created_at": now,
            "created_by": admin_id
        }
        
        db.collection("platform_messages").document(message_id).set(message_dict)
        return PlatformMessageResponse(**message_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error sending message: {str(e)}")

@router.get("/messages", response_model=List[PlatformMessageResponse])
def get_platform_messages(admin_id: str, limit: int = 50):
    # get all platform messages
    check_admin_role(admin_id)
    try:
        messages = db.collection("platform_messages").order_by("created_at", direction="DESCENDING").limit(limit).stream()
        return [PlatformMessageResponse(**msg.to_dict()) for msg in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@router.get("/reports", response_model=ReportData)
def get_platform_reports(admin_id: str):
    # get platform activity reports
    check_admin_role(admin_id)
    try:
        # count users
        users = list(db.collection("users").stream())
        total_users = len(users)
        
        # count swaps
        swaps = list(db.collection("swaps").stream())
        total_swaps = len(swaps)
        pending_swaps = len([s for s in swaps if s.to_dict().get("status") == "pending"])
        completed_swaps = len([s for s in swaps if s.to_dict().get("status") == "completed"])
        
        # calculate average rating
        reviews = list(db.collection("reviews").stream())
        if reviews:
            ratings = [r.to_dict().get("rating", 0) for r in reviews]
            average_rating = sum(ratings) / len(ratings)
        else:
            average_rating = 0.0
        
        # recent activity (last 10 swaps)
        recent_swaps = db.collection("swaps").order_by("created_at", direction="DESCENDING").limit(10).stream()
        recent_activity = []
        for swap in recent_swaps:
            swap_data = swap.to_dict()
            recent_activity.append({
                "type": "swap",
                "id": swap_data.get("id"),
                "status": swap_data.get("status"),
                "created_at": swap_data.get("created_at")
            })
        
        return ReportData(
            total_users=total_users,
            total_swaps=total_swaps,
            pending_swaps=pending_swaps,
            completed_swaps=completed_swaps,
            average_rating=round(average_rating, 2),
            recent_activity=recent_activity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating reports: {str(e)}")

@router.get("/users")
def get_all_users(admin_id: str, banned: Optional[bool] = None, limit: int = 100):
    # get all users for admin management
    check_admin_role(admin_id)
    try:
        query = db.collection("users")
        if banned is not None:
            query = query.where("is_banned", "==", banned)
        
        users = query.limit(limit).stream()
        return [user.to_dict() for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.delete("/message/{message_id}")
def delete_platform_message(message_id: str, admin_id: str):
    # delete a platform message
    check_admin_role(admin_id)
    try:
        db.collection("platform_messages").document(message_id).delete()
        return {"message": "Platform message deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting message: {str(e)}")

@router.get("/stats", response_model=AdminStats)
def get_admin_dashboard_stats(admin_id: str):
    # get comprehensive stats for admin dashboard
    check_admin_role(admin_id)
    try:
        # get all users
        users = list(db.collection("users").stream())
        total_users = len(users)
        banned_users = len([u for u in users if u.to_dict().get("is_banned", False)])
        
        # recent signups (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_signups = 0
        for user in users:
            user_data = user.to_dict()
            created_at = user_data.get("created_at")
            if created_at:
                # Handle both datetime objects and strings
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    except:
                        continue
                elif hasattr(created_at, 'replace'):
                    # If it's already a datetime, make it UTC aware if needed
                    if created_at.tzinfo is None:
                        created_at = created_at.replace(tzinfo=None)
                    
                # Compare dates (both should be naive now)
                if created_at and created_at.replace(tzinfo=None) > thirty_days_ago:
                    recent_signups += 1
        
        # get all swaps
        swaps = list(db.collection("swaps").stream())
        total_swaps = len(swaps)
        pending_swaps = len([s for s in swaps if s.to_dict().get("status") == "pending"])
        completed_swaps = len([s for s in swaps if s.to_dict().get("status") == "completed"])
        
        # calculate average rating
        reviews = list(db.collection("reviews").stream())
        if reviews:
            ratings = [r.to_dict().get("rating", 0) for r in reviews]
            average_rating = sum(ratings) / len(ratings)
        else:
            average_rating = 0.0
        
        # count platform messages
        messages = list(db.collection("platform_messages").stream())
        platform_messages = len(messages)
        
        return AdminStats(
            total_users=total_users,
            banned_users=banned_users,
            total_swaps=total_swaps,
            pending_swaps=pending_swaps,
            completed_swaps=completed_swaps,
            average_rating=round(average_rating, 2),
            platform_messages=platform_messages,
            recent_signups=recent_signups
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating stats: {str(e)}")
        return {"message": "Platform message deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting message: {str(e)}")
