from fastapi import APIRouter
from typing import Optional
from local_market import get_local_businesses, get_businesses_near_alternative
from hidden_gems import get_hidden_gems

local_router = APIRouter(prefix="/local", tags=["Local Market & Hidden Gems"])

@local_router.get("/businesses/{destination_id}")
def api_get_businesses(destination_id: str, category: Optional[str] = None):
    return get_local_businesses(destination_id, category)

@local_router.get("/hidden-gems")
def api_get_hidden_gems(exclude_top: int = 3):
    return get_hidden_gems(exclude_top)

@local_router.get("/businesses-near-alternative/{destination_id}")
def api_get_businesses_near_alt(destination_id: str):
    return get_businesses_near_alternative(destination_id)
