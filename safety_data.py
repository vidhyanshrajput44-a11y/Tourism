import json
from dataclasses import dataclass
from typing import List, Dict, Any
import math

@dataclass
class RiskZone:
    risk_zone_id: str
    destination_id: str
    latitude: float
    longitude: float
    radius_meters: float
    risk_type: str
    risk_level: str

@dataclass
class HelpPoint:
    help_point_id: str
    destination_id: str
    type: str  # hospital or police
    name: str
    latitude: float
    longitude: float
    phone_number: str

# Dummy static seeded dataset near the destinations
# We will just generate some points slightly offset from the main destination coords
DESTINATIONS_COORDS = {
    "taj_mahal": (27.1751, 78.0421),
    "jaipur_city_palace": (26.9255, 75.8236),
    "goa_baga_beach": (15.5619, 73.7553),
    "kerala_backwaters": (9.4981, 76.3388),
    "varanasi_ghats": (25.3109, 83.0107),
    "hampi_ruins": (15.3350, 76.4600),
    "manali": (32.2432, 77.1892),
    "mysore_palace": (12.3052, 76.6551),
}

def generate_safety_data() -> (List[RiskZone], List[HelpPoint]):
    risk_zones = []
    help_points = []
    
    for dest_id, (lat, lon) in DESTINATIONS_COORDS.items():
        # Add 2 risk zones for each destination
        risk_zones.extend([
            RiskZone(
                risk_zone_id=f"rz_{dest_id}_1",
                destination_id=dest_id,
                latitude=lat + 0.005,
                longitude=lon + 0.005,
                radius_meters=300.0,
                risk_type="poor_lighting",
                risk_level="Medium"
            ),
            RiskZone(
                risk_zone_id=f"rz_{dest_id}_2",
                destination_id=dest_id,
                latitude=lat - 0.008,
                longitude=lon - 0.003,
                radius_meters=500.0,
                risk_type="isolated_area",
                risk_level="High"
            )
        ])
        
        # Add 1 hospital and 1 police station
        help_points.extend([
            HelpPoint(
                help_point_id=f"hp_{dest_id}_hosp",
                destination_id=dest_id,
                type="hospital",
                name=f"City General Hospital ({dest_id})",
                latitude=lat + 0.015,
                longitude=lon - 0.010,
                phone_number="+91-800-HOSPITAL"
            ),
            HelpPoint(
                help_point_id=f"hp_{dest_id}_pol",
                destination_id=dest_id,
                type="police",
                name=f"Tourist Police Station ({dest_id})",
                latitude=lat - 0.012,
                longitude=lon + 0.012,
                phone_number="+91-100"
            )
        ])
        
    return risk_zones, help_points

RISK_ZONES, HELP_POINTS = generate_safety_data()

def get_risk_zones(destination_id: str) -> List[RiskZone]:
    return [rz for rz in RISK_ZONES if rz.destination_id == destination_id]

def get_help_points(destination_id: str) -> List[HelpPoint]:
    return [hp for hp in HELP_POINTS if hp.destination_id == destination_id]
