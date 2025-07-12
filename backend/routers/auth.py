from fastapi import APIRouter, HTTPException, Depends
from firebase_init import db
from models import UserCreate, UserResponse, UserRole
from typing import Optional
from datetime import datetime
import uuid
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])

def check_db_connection():
    # make sure firebase is working
    if db is None:
        raise HTTPException(
            status_code=500, 
            detail="Database connection not available. Please check Firebase configuration."
        )

def hash_password(password: str) -> str:
    # simple password hashing - in real app use proper bcrypt
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, password: str):
    # register new user
    check_db_connection()
    try:
        # check if email already exists
        existing_users = db.collection("users").where("email", "==", user_data.email).stream()
        if len(list(existing_users)) > 0:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # create new user
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        hashed_password = hash_password(password)
        
        user_dict = {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "password_hash": hashed_password,  # store hashed password
            "location": user_data.location,
            "bio": user_data.bio,
            "skills_offered": [skill.dict() for skill in user_data.skills_offered],
            "skills_wanted": [skill.dict() for skill in user_data.skills_wanted],
            "availability": user_data.availability.dict() if user_data.availability else None,
            "is_profile_public": user_data.is_profile_public,
            "profile_photo_url": None,
            "rating": None,
            "total_swaps": 0,
            "role": UserRole.USER,
            "is_banned": False,
            "created_at": now,
            "updated_at": now
        }
        
        db.collection("users").document(user_id).set(user_dict)
        
        # don't return password hash
        user_dict.pop("password_hash", None)
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

@router.post("/login")
def login_user(email: str, password: str):
    # login user
    check_db_connection()
    try:
        # find user by email
        users = db.collection("users").where("email", "==", email).stream()
        user_list = list(users)
        
        if not user_list:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user_data = user_list[0].to_dict()
        
        # check if user is banned
        if user_data.get("is_banned", False):
            raise HTTPException(status_code=403, detail="Account has been banned")
        
        # verify password
        hashed_password = hash_password(password)
        if user_data.get("password_hash") != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # in real app, generate JWT token here
        user_data.pop("password_hash", None)  # don't return password hash
        return {
            "message": "Login successful", 
            "user": user_data,
            "token": f"fake_jwt_token_for_{user_data['id']}"  # placeholder token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

@router.post("/logout")
def logout_user(user_id: str):
    # logout user (invalidate token in real app)
    return {"message": "Logout successful"}

@router.get("/me")
def get_current_user(user_id: str):
    # get current user info
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user_doc.to_dict()
        user_data.pop("password_hash", None)  # don't return password hash
        return user_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@router.post("/change-password")
def change_password(user_id: str, old_password: str, new_password: str):
    # change user password
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user_doc.to_dict()
        
        # verify old password
        old_hashed = hash_password(old_password)
        if user_data.get("password_hash") != old_hashed:
            raise HTTPException(status_code=401, detail="Current password is incorrect")
        
        # update to new password
        new_hashed = hash_password(new_password)
        db.collection("users").document(user_id).update({
            "password_hash": new_hashed,
            "updated_at": datetime.utcnow()
        })
        
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error changing password: {str(e)}")

@router.delete("/delete-account")
def delete_account(user_id: str, password: str):
    # delete user account
    check_db_connection()
    try:
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user_doc.to_dict()
        
        # verify password
        hashed_password = hash_password(password)
        if user_data.get("password_hash") != hashed_password:
            raise HTTPException(status_code=401, detail="Password is incorrect")
        
        # delete user and related data
        db.collection("users").document(user_id).delete()
        
        # also delete user's swaps and reviews
        user_swaps = db.collection("swaps").where("requester_id", "==", user_id).stream()
        for swap in user_swaps:
            swap.reference.delete()
            
        user_swaps = db.collection("swaps").where("requestee_id", "==", user_id).stream()
        for swap in user_swaps:
            swap.reference.delete()
            
        user_reviews = db.collection("reviews").where("reviewer_id", "==", user_id).stream()
        for review in user_reviews:
            review.reference.delete()
        
        return {"message": "Account deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting account: {str(e)}")
