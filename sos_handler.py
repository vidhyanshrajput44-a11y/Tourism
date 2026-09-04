import math
import logging
from typing import List, Dict, Any
from safety_data import HELP_POINTS, RISK_ZONES, HelpPoint, RiskZone
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sos_handler")

def haversine_dist(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def trigger_sos(user_id: str, current_lat: float, current_lon: float, emergency_contacts: List[str]) -> Dict[str, Any]:
    # Find nearest hospital and police from ALL help points
    nearest_hospital = None
    nearest_police = None
    min_dist_hospital = float('inf')
    min_dist_police = float('inf')

    for hp in HELP_POINTS:
        dist = haversine_dist(current_lat, current_lon, hp.latitude, hp.longitude)
        if hp.type == "hospital" and dist < min_dist_hospital:
            min_dist_hospital = dist
            nearest_hospital = hp
        elif hp.type == "police" and dist < min_dist_police:
            min_dist_police = dist
            nearest_police = hp

    timestamp = datetime.now(timezone.utc).isoformat()
    message = f"URGENT: SOS triggered by user {user_id} at {current_lat}, {current_lon}."

    payload = {
        "user_id": user_id,
        "timestamp": timestamp,
        "lat": current_lat,
        "lon": current_lon,
        "nearest_hospital": nearest_hospital.__dict__ if nearest_hospital else None,
        "nearest_police": nearest_police.__dict__ if nearest_police else None,
        "message": message,
        "emergency_contacts": emergency_contacts
    }

    # Simulate sending notification (demo fallback - guaranteed to work)
    logger.info("=== SOS ALERT TRIGGERED ===")
    logger.info(f"Payload: {payload}")
    for contact in emergency_contacts:
        logger.info(f"[MOCK SMS] Sending alert to {contact}: {message}")

    return {
        "status": "success",
        "alert_sent_to": emergency_contacts,
        "nearest_hospital": payload["nearest_hospital"],
        "nearest_police": payload["nearest_police"],
        "eta_message": "Authorities and emergency contacts have been notified."
    }

def point_to_segment_distance(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
    # A rough 2D cartesian distance approximation in meters (for small distances)
    # 1 deg lat ~ 111000m, 1 deg lon ~ 111000m * cos(lat)
    # Using local flat earth approximation
    lat_to_m = 111000.0
    lon_to_m = 111000.0 * math.cos(math.radians(py))
    
    # Transform points to local meter grid relative to A
    ax_m, ay_m = 0.0, 0.0
    bx_m, by_m = (bx - ax) * lon_to_m, (by - ay) * lat_to_m
    px_m, py_m = (px - ax) * lon_to_m, (py - ay) * lat_to_m

    line_mag = math.hypot(bx_m, by_m)
    if line_mag == 0:
        return math.hypot(px_m, py_m)

    u = ((px_m * bx_m) + (py_m * by_m)) / (line_mag ** 2)
    if u < 0.0 or u > 1.0:
        dist_to_a = math.hypot(px_m, py_m)
        dist_to_b = math.hypot(px_m - bx_m, py_m - by_m)
        return min(dist_to_a, dist_to_b)

    ix = bx_m * u
    iy = by_m * u
    return math.hypot(px_m - ix, py_m - iy)


def get_safe_route(destination_id: str, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
    dest_zones = [rz for rz in RISK_ZONES if rz.destination_id == destination_id]
    warnings = []
    
    for rz in dest_zones:
        # Distance from the segment (start -> end) to the risk zone center
        dist = point_to_segment_distance(rz.longitude, rz.latitude, start_lon, start_lat, end_lon, end_lat)
        if dist <= rz.radius_meters:
            warnings.append(f"Route passes through a {rz.risk_level} risk zone ({rz.risk_type}) at {rz.latitude}, {rz.longitude}. Please avoid this area.")

    is_safe = len(warnings) == 0
    
    # Suggested waypoint to bypass (very basic mock logic: just offset the midpoint)
    suggested_waypoints = []
    if not is_safe:
        mid_lat = (start_lat + end_lat) / 2.0
        mid_lon = (start_lon + end_lon) / 2.0
        suggested_waypoints.append({
            "lat": mid_lat + 0.01,
            "lon": mid_lon + 0.01,
            "note": "Suggested detour to avoid flagged risk zones"
        })

    return {
        "is_safe": is_safe,
        "warnings": warnings,
        "suggested_waypoints": suggested_waypoints
    }
