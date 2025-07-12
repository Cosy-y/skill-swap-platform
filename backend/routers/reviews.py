from fastapi import APIRouter, HTTPException, Query
from firebase_init import db
from models import ReviewCreate, ReviewResponse, ReviewUpdate
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def check_db_connection():
    # make sure firebase is working
    if db is None:
        raise HTTPException(
            status_code=500, 
            detail="Database connection not available. Please check Firebase configuration."
        )

@router.post("/", response_model=ReviewResponse)
def create_review(review_data: ReviewCreate, reviewer_id: str):
    # create review after completed swap
    check_db_connection()
    try:
        # check if swap exists and is completed
        swap_doc = db.collection("swaps").document(review_data.swap_id).get()
        if not swap_doc.exists:
            raise HTTPException(status_code=404, detail="Swap not found")
        
        swap_data = swap_doc.to_dict()
        if swap_data["status"] != "completed":
            raise HTTPException(status_code=400, detail="Can only review completed swaps")
        
        # check if reviewer was part of the swap
        if reviewer_id not in [swap_data["requester_id"], swap_data["requestee_id"]]:
            raise HTTPException(status_code=403, detail="Only swap participants can leave reviews")
        
        # check if review already exists
        existing_reviews = db.collection("reviews").where("swap_id", "==", review_data.swap_id).where("reviewer_id", "==", reviewer_id).stream()
        if len(list(existing_reviews)) > 0:
            raise HTTPException(status_code=400, detail="You already reviewed this swap")
        
        # create the review
        review_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        review_dict = {
            "id": review_id,
            "swap_id": review_data.swap_id,
            "reviewer_id": reviewer_id,
            "reviewee_id": review_data.reviewee_id,
            "rating": review_data.rating,
            "comment": review_data.comment,
            "created_at": now
        }
        
        db.collection("reviews").document(review_id).set(review_dict)
        
        # update user rating
        update_user_rating(review_data.reviewee_id)
        
        return ReviewResponse(**review_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating review: {str(e)}")

@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(user_id: str, limit: int = Query(20, le=50)):
    # get all reviews for a user
    check_db_connection()
    try:
        reviews = db.collection("reviews").where("reviewee_id", "==", user_id).limit(limit).stream()
        return [ReviewResponse(**review.to_dict()) for review in reviews]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reviews: {str(e)}")

@router.get("/swap/{swap_id}", response_model=List[ReviewResponse])
def get_swap_reviews(swap_id: str):
    # get reviews for a specific swap
    check_db_connection()
    try:
        reviews = db.collection("reviews").where("swap_id", "==", swap_id).stream()
        return [ReviewResponse(**review.to_dict()) for review in reviews]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching swap reviews: {str(e)}")

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: str, review_update: ReviewUpdate, user_id: str):
    # update a review
    check_db_connection()
    try:
        review_doc = db.collection("reviews").document(review_id).get()
        if not review_doc.exists:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review_data = review_doc.to_dict()
        
        # only reviewer can update their review
        if user_id != review_data["reviewer_id"]:
            raise HTTPException(status_code=403, detail="Only reviewer can update their review")
        
        # update the review
        update_data = {}
        if review_update.rating:
            update_data["rating"] = review_update.rating
        if review_update.comment is not None:
            update_data["comment"] = review_update.comment
            
        if update_data:
            db.collection("reviews").document(review_id).update(update_data)
            
            # recalculate user rating if rating changed
            if "rating" in update_data:
                update_user_rating(review_data["reviewee_id"])
        
        # return updated review
        updated_doc = db.collection("reviews").document(review_id).get()
        return ReviewResponse(**updated_doc.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating review: {str(e)}")

@router.delete("/{review_id}")
def delete_review(review_id: str, user_id: str):
    # delete a review
    check_db_connection()
    try:
        review_doc = db.collection("reviews").document(review_id).get()
        if not review_doc.exists:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review_data = review_doc.to_dict()
        
        # only reviewer can delete their review
        if user_id != review_data["reviewer_id"]:
            raise HTTPException(status_code=403, detail="Only reviewer can delete their review")
        
        db.collection("reviews").document(review_id).delete()
        
        # recalculate user rating
        update_user_rating(review_data["reviewee_id"])
        
        return {"message": "Review deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting review: {str(e)}")

def update_user_rating(user_id: str):
    # helper function to recalculate user rating
    try:
        reviews = db.collection("reviews").where("reviewee_id", "==", user_id).stream()
        ratings = [review.to_dict()["rating"] for review in reviews]
        
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            db.collection("users").document(user_id).update({"rating": round(avg_rating, 2)})
        else:
            db.collection("users").document(user_id).update({"rating": None})
    except Exception as e:
        print(f"Error updating user rating: {e}")  # just log it, don't fail the main operation
