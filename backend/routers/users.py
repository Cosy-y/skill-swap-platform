from fastapi import APIRouter
from backend.firebase_init import db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    users = db.collection("users").stream()
    return [user.to_dict() for user in users]
