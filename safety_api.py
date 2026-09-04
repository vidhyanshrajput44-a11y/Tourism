from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from safety_data import get_risk_zones, get_help_points
from sos_handler import trigger_sos, get_safe_route

safety_router = APIRouter(prefix="/safety", tags=["Safety & SOS"])

class SOSRequest(BaseModel):
    user_id: str
    lat: float
    lon: float
    emergency_contacts: List[str]

class RouteRequest(BaseModel):
    destination_id: str
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float

@safety_router.post("/sos")
def handle_sos(req: SOSRequest):
    return trigger_sos(
        user_id=req.user_id,
        current_lat=req.lat,
        current_lon=req.lon,
        emergency_contacts=req.emergency_contacts
    )

@safety_router.get("/risk-zones/{destination_id}")
def handle_get_risk_zones(destination_id: str):
    return get_risk_zones(destination_id)

@safety_router.get("/help-points/{destination_id}")
def handle_get_help_points(destination_id: str):
    return get_help_points(destination_id)

@safety_router.post("/safe-route")
def handle_safe_route(req: RouteRequest):
    return get_safe_route(
        destination_id=req.destination_id,
        start_lat=req.start_lat,
        start_lon=req.start_lon,
        end_lat=req.end_lat,
        end_lon=req.end_lon
    )
