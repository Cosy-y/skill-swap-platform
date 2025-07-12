from fastapi import APIRouter, HTTPException, Query
from firebase_init import db
from models import UserCreate, UserUpdate, UserResponse, UserPublicResponse
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

def check_db_connection():
    # just making sure firebase works
    if db is None:
        raise HTTPException(status_code=500, detail="Database broke :(")

@router.get("/", response_model=List[UserPublicResponse])
def get_public_users(
    skill: Optional[str] = Query(None, description="Filter by skill name"),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(20, le=100, description="Limit number of results")
):
    # gets all the users to show on homepage
    check_db_connection()
    try:
        query = db.collection("users").where("is_profile_public", "==", True)
        
        if skill:
            # basic skill search - not very good but works
            query = query.where("skills_offered", "array_contains_any", [skill])
        
        if location:
            query = query.where("location", "==", location)
            
        users = query.limit(limit).stream()
        return [UserPublicResponse(**user.to_dict()) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate):
    # make new user 
    check_db_connection()
    try:
        user_id = str(uuid.uuid4())  # random id
        now = datetime.utcnow()
        
        user_dict = user_data.dict()
        user_dict.update({
            "id": user_id,
            "rating": None,  # no rating yet
            "total_swaps": 0,  # hasn't done any swaps
            "created_at": now,
            "updated_at": now
        })
        
        db.collection("users").document(user_id).set(user_dict)
        return UserResponse(**user_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get a specific user by ID"""
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user_doc.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_data: UserUpdate):
    """Update a user profile"""
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Only update fields that are provided
        update_data = {k: v for k, v in user_data.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        db.collection("users").document(user_id).update(update_data)
        
        # Return updated user
        updated_doc = db.collection("users").document(user_id).get()
        return UserResponse(**updated_doc.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")

@router.delete("/{user_id}")
def delete_user(user_id: str):
    """Delete a user profile"""
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.collection("users").document(user_id).delete()
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

@router.get("/{user_id}/public", response_model=UserPublicResponse)  
def get_user_public_profile(user_id: str):
    """Get public view of a user profile"""
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user_doc.to_dict()
        if not user_data.get("is_profile_public", True):
            raise HTTPException(status_code=403, detail="Profile is private")
            
        return UserPublicResponse(**user_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@router.get("/search/skills")
def search_users_by_skill(skill_name: str, skill_type: str = Query(..., regex="^(offered|wanted)$")):
    """Search users by specific skill they offer or want"""
    check_db_connection()
    try:
        field_name = f"skills_{skill_type}"
        
        # Note: This is a simplified search. For production, you'd want to use 
        # Firestore's array-contains or implement a proper search solution
        users = db.collection("users").where("is_profile_public", "==", True).stream()
        
        matching_users = []
        for user in users:
            user_data = user.to_dict()
            skills = user_data.get(field_name, [])
            
            # Check if any skill matches (case-insensitive)
            for skill in skills:
                if skill_name.lower() in skill.get("name", "").lower():
                    matching_users.append(UserPublicResponse(**user_data))
                    break
        
        return matching_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching users: {str(e)}")
