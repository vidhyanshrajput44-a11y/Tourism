"""
FastAPI router for UI 8 - Photo-Based Heritage Rewards + Booking Redemption.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List

from heritage_rewards_data import MONUMENTS_DB
from rewards_engine import submit_photo, get_user_points, get_available_rewards, redeem_reward
from booking_redirect import build_makemytrip_url, simulate_partner_booking

rewards_router = APIRouter(prefix="/rewards", tags=["UI 8 - Heritage Rewards"])

class RedeemRequest(BaseModel):
    user_id: str
    tier_id: str

class MockBookingRequest(BaseModel):
    user_id: str
    hotel_name: str
    discount_code: str
    discount_pct: int

@rewards_router.get("/monuments/{destination_id}")
def get_monuments_for_dest(destination_id: str):
    monuments = MONUMENTS_DB.get(destination_id, [])
    return monuments

@rewards_router.post("/submit-photo")
async def api_submit_photo(
    user_id: str = Form(...),
    monument_id: str = Form(...),
    destination_id: str = Form(...),
    force_verify: bool = Form(False),
    image: UploadFile = File(...)
):
    try:
        # In a real app we'd save the image. For this, we just use the filename.
        filename = image.filename
        res = submit_photo(user_id, monument_id, destination_id, filename, force_verify)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rewards_router.get("/my-points/{user_id}")
def api_get_points(user_id: str):
    return get_user_points(user_id)

@rewards_router.get("/available-tiers/{user_id}")
def api_available_tiers(user_id: str):
    return get_available_rewards(user_id)

@rewards_router.post("/redeem")
def api_redeem_reward(req: RedeemRequest):
    try:
        return redeem_reward(req.user_id, req.tier_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@rewards_router.get("/book/makemytrip-link")
def api_makemytrip_link(destination_id: str, checkin: str = "", checkout: str = ""):
    url = build_makemytrip_url(destination_id, checkin, checkout)
    return {"url": url}

@rewards_router.post("/book/partner-preview")
def api_partner_preview(req: MockBookingRequest):
    res = simulate_partner_booking(req.user_id, req.hotel_name, req.discount_code, req.discount_pct)
    return res
