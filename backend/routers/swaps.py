from fastapi import APIRouter, HTTPException, Query
from firebase_init import db
from models import SwapCreate, SwapUpdate, SwapResponse, SwapStatus
from google.cloud import firestore
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/swaps", tags=["Swaps"])

def check_db_connection():
    # make sure firebase is connected
    if db is None:
        raise HTTPException(
            status_code=500, 
            detail="Database connection not available. Please check Firebase configuration."
        )

@router.post("/", response_model=SwapResponse)
def create_swap_request(swap_data: SwapCreate, requester_id: str = Query(..., description="ID of the user making the request")):
    # create new swap request
    check_db_connection()
    try:
        # check if both users actually exist
        requester = db.collection("users").document(requester_id).get()
        requestee = db.collection("users").document(swap_data.requestee_id).get()
        
        if not requester.exists:
            raise HTTPException(status_code=404, detail="Requester not found")
        if not requestee.exists:
            raise HTTPException(status_code=404, detail="Requestee not found")
        
        # make the swap request
        swap_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        swap_dict = {
            "id": swap_id,
            "requester_id": requester_id,
            "requestee_id": swap_data.requestee_id,
            "requester_skill": swap_data.requester_skill,
            "requested_skill": swap_data.requested_skill,
            "message": swap_data.message,
            "status": SwapStatus.PENDING,
            "created_at": now,
            "updated_at": now
        }
        
        db.collection("swaps").document(swap_id).set(swap_dict)
        return SwapResponse(**swap_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating swap request: {str(e)}")

@router.get("/user/{user_id}", response_model=List[SwapResponse])
def get_user_swaps(
    user_id: str,
    status: Optional[SwapStatus] = Query(None, description="Filter by swap status"),
    as_requester: Optional[bool] = Query(None, description="Filter swaps where user is requester"),
    limit: int = Query(50, le=100)
):
    # get all swaps for a specific user
    check_db_connection()
    try:
        swaps_collection = db.collection("swaps")
        
        if as_requester is True:
            query = swaps_collection.where("requester_id", "==", user_id)
        elif as_requester is False:
            query = swaps_collection.where("requestee_id", "==", user_id)
        else:
            # get swaps where user is either requester or requestee
            requester_swaps = list(swaps_collection.where("requester_id", "==", user_id).limit(limit//2).stream())
            requestee_swaps = list(swaps_collection.where("requestee_id", "==", user_id).limit(limit//2).stream())
            
            all_swaps = requester_swaps + requestee_swaps
            if status:
                all_swaps = [swap for swap in all_swaps if swap.to_dict().get("status") == status]
            
            return [SwapResponse(**swap.to_dict()) for swap in all_swaps[:limit]]
        
        if status:
            query = query.where("status", "==", status)
            
        swaps = query.limit(limit).stream()
        return [SwapResponse(**swap.to_dict()) for swap in swaps]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching swaps: {str(e)}")

@router.get("/{swap_id}", response_model=SwapResponse)
def get_swap(swap_id: str):
    # get a specific swap by id
    check_db_connection()
    try:
        swap_doc = db.collection("swaps").document(swap_id).get()
        if not swap_doc.exists:
            raise HTTPException(status_code=404, detail="Swap not found")
        return SwapResponse(**swap_doc.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching swap: {str(e)}")

@router.put("/{swap_id}", response_model=SwapResponse)
def update_swap_status(swap_id: str, swap_update: SwapUpdate, user_id: str = Query(..., description="ID of the user updating the swap")):
    # update swap status (accept, reject, etc)
    check_db_connection()
    try:
        swap_doc = db.collection("swaps").document(swap_id).get()
        if not swap_doc.exists:
            raise HTTPException(status_code=404, detail="Swap not found")
        
        swap_data = swap_doc.to_dict()
        
        # only requestee can accept/reject, only requester can cancel
        if swap_update.status in [SwapStatus.ACCEPTED, SwapStatus.REJECTED]:
            if user_id != swap_data["requestee_id"]:
                raise HTTPException(status_code=403, detail="Only requestee can accept/reject swaps")
        elif swap_update.status == SwapStatus.CANCELLED:
            if user_id not in [swap_data["requester_id"], swap_data["requestee_id"]]:
                raise HTTPException(status_code=403, detail="Only participants can cancel swaps")
        
        # update the swap
        update_data = {
            "status": swap_update.status,
            "updated_at": datetime.utcnow()
        }
        if swap_update.message:
            update_data["message"] = swap_update.message
            
        db.collection("swaps").document(swap_id).update(update_data)
        
        # if swap is completed, increment user swap counts
        if swap_update.status == SwapStatus.COMPLETED:
            db.collection("users").document(swap_data["requester_id"]).update({
                "total_swaps": firestore.Increment(1)
            })
            db.collection("users").document(swap_data["requestee_id"]).update({
                "total_swaps": firestore.Increment(1)
            })
        
        # return updated swap
        updated_doc = db.collection("swaps").document(swap_id).get()
        return SwapResponse(**updated_doc.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating swap: {str(e)}")

@router.delete("/{swap_id}")
def delete_swap_request(swap_id: str, user_id: str = Query(..., description="ID of the user deleting the swap")):
    # delete a swap request (only if pending and user is requester)
    check_db_connection()
    try:
        swap_doc = db.collection("swaps").document(swap_id).get()
        if not swap_doc.exists:
            raise HTTPException(status_code=404, detail="Swap not found")
        
        swap_data = swap_doc.to_dict()
        
        # only requester can delete, and only if pending
        if user_id != swap_data["requester_id"]:
            raise HTTPException(status_code=403, detail="Only requester can delete swap requests")
        
        if swap_data["status"] != SwapStatus.PENDING:
            raise HTTPException(status_code=400, detail="Can only delete pending swap requests")
        
        db.collection("swaps").document(swap_id).delete()
        return {"message": "Swap request deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting swap: {str(e)}")

@router.get("/pending/count/{user_id}")
def get_pending_swaps_count(user_id: str):
    # get count of pending swaps for a user
    check_db_connection()
    try:
        # count swaps where user is requestee and status is pending
        pending_swaps = db.collection("swaps").where("requestee_id", "==", user_id).where("status", "==", SwapStatus.PENDING).stream()
        count = len(list(pending_swaps))
        return {"pending_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting pending swaps: {str(e)}")
