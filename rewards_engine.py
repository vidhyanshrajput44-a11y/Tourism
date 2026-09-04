"""
Rewards and Redemption Logic for Heritage Rewards.
"""

import uuid
from datetime import datetime, timedelta
import random
import string

from heritage_rewards_data import (
    init_user_ledger, user_points_ledger, user_photo_submissions, 
    REWARD_TIERS, get_monument
)
from photo_verifier import verify_monument_photo

def submit_photo(user_id: str, monument_id: str, destination_id: str, image_file_name: str, force_verify: bool = False):
    init_user_ledger(user_id)
    
    monument = get_monument(monument_id)
    if not monument:
        raise ValueError("Invalid monument ID")
        
    is_plausible, confidence, reason = verify_monument_photo(image_file_name, monument_id, force_verify)
    
    submission_id = str(uuid.uuid4())
    status = "verified" if is_plausible else "pending_manual_review"
    points_awarded = monument["points_value"] if is_plausible else 0
    
    submission = {
        "submission_id": submission_id,
        "user_id": user_id,
        "monument_id": monument_id,
        "destination_id": destination_id,
        "monument_name": monument["name"],
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "points_awarded": points_awarded,
        "verification_reason": reason,
        "confidence": confidence
    }
    
    user_photo_submissions.append(submission)
    
    if is_plausible:
        user_points_ledger[user_id]["total_points"] += points_awarded
        user_points_ledger[user_id]["current_balance"] += points_awarded
        
    return submission

def get_user_points(user_id: str):
    init_user_ledger(user_id)
    user_history = sorted(
        [s for s in user_photo_submissions if s["user_id"] == user_id],
        key=lambda x: x["timestamp"], reverse=True
    )
    
    return {
        "ledger": user_points_ledger[user_id],
        "history": user_history
    }

def get_available_rewards(user_id: str):
    init_user_ledger(user_id)
    balance = user_points_ledger[user_id]["current_balance"]
    
    available = []
    for tier in REWARD_TIERS:
        t_copy = tier.copy()
        t_copy["is_eligible"] = (balance >= tier["points_required"])
        available.append(t_copy)
        
    return available

def redeem_reward(user_id: str, tier_id: str):
    init_user_ledger(user_id)
    
    tier = next((t for t in REWARD_TIERS if t["tier_id"] == tier_id), None)
    if not tier:
        raise ValueError("Invalid reward tier")
        
    if user_points_ledger[user_id]["current_balance"] < tier["points_required"]:
        raise ValueError("Insufficient points balance")
        
    user_points_ledger[user_id]["current_balance"] -= tier["points_required"]
    user_points_ledger[user_id]["points_redeemed"] += tier["points_required"]
    
    # Generate discount code
    code = f"FOOTPRINT-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    
    return {
        "discount_code": code,
        "discount_pct": tier["discount_pct"],
        "tier_name": tier["name"],
        "valid_until": (datetime.now() + timedelta(days=90)).isoformat()
    }
