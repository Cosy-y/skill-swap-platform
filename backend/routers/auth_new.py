from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from firebase_init import db
from models import LoginRequest, UserCreate, UserResponse, SuccessResponse
from typing import Optional
from datetime import datetime
import uuid
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Simple password hashing - in production use proper hashing like bcrypt"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def create_custom_token(user_id: str) -> str:
    """Create a custom Firebase auth token"""
    try:
        custom_token = auth.create_custom_token(user_id)
        return custom_token.decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify Firebase ID token and return user ID"""
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token['uid']
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

@router.post("/register", response_model=SuccessResponse)
def register_user(user_data: UserCreate):
    """Register a new user"""
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Check if email already exists
        existing_users = db.collection("users").where("email", "==", user_data.email).get()
        if len(existing_users) > 0:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user document
        user_id = str(uuid.uuid4())
        user_doc = {
            "user_id": user_id,
            "email": user_data.email,
            "password_hash": hash_password(user_data.password),
            "full_name": user_data.full_name,
            "location": user_data.location,
            "bio": user_data.bio,
            "skills_offered": [skill.dict() for skill in user_data.skills_offered],
            "skills_wanted": [skill.dict() for skill in user_data.skills_wanted],
            "availability": user_data.availability,
            "is_profile_public": user_data.is_profile_public,
            "profile_image_url": None,
            "rating": 0.0,
            "total_swaps": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Create Firebase Auth user
        firebase_user = auth.create_user(
            uid=user_id,
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.full_name
        )
        
        # Save to Firestore
        db.collection("users").document(user_id).set(user_doc)
        
        # Create custom token
        custom_token = create_custom_token(user_id)
        
        return SuccessResponse(
            message="User registered successfully",
            data={
                "user_id": user_id,
                "custom_token": custom_token
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=SuccessResponse)
def login_user(login_data: LoginRequest):
    """Login user and return custom token"""
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        # Find user by email
        users = db.collection("users").where("email", "==", login_data.email).get()
        if len(users) == 0:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user_doc = users[0]
        user_data = user_doc.to_dict()
        
        # Verify password
        if not verify_password(login_data.password, user_data["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create custom token
        custom_token = create_custom_token(user_data["user_id"])
        
        return SuccessResponse(
            message="Login successful",
            data={
                "user_id": user_data["user_id"],
                "custom_token": custom_token,
                "user_name": user_data["full_name"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: str = Depends(verify_token)):
    """Get current user profile"""
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        user_doc = db.collection("users").document(current_user).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user_doc.to_dict()
        
        # Convert to response model
        return UserResponse(
            user_id=user_data["user_id"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            location=user_data.get("location"),
            bio=user_data.get("bio"),
            skills_offered=user_data.get("skills_offered", []),
            skills_wanted=user_data.get("skills_wanted", []),
            availability=user_data.get("availability", {}),
            is_profile_public=user_data.get("is_profile_public", True),
            profile_image_url=user_data.get("profile_image_url"),
            rating=user_data.get("rating", 0.0),
            total_swaps=user_data.get("total_swaps", 0),
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

@router.post("/verify-token", response_model=SuccessResponse)
def verify_user_token(current_user: str = Depends(verify_token)):
    """Verify if token is valid"""
    return SuccessResponse(
        message="Token is valid",
        data={"user_id": current_user}
    )
