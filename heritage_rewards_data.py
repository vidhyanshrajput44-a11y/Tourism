"""
Data layer for UI 8 - Photo-Based Heritage Rewards + Booking Redemption.
"""

from typing import List, Dict, Any
from datetime import datetime
import uuid

# Define monuments for each destination (reusing UI 1 destination IDs)
MONUMENTS_DB = {
    "taj_mahal": [
        {"monument_id": "m_taj_1", "name": "Taj Mahal Main Mausoleum", "points_value": 200, "description": "The central white marble structure."},
        {"monument_id": "m_taj_2", "name": "Taj Mahal Mosque", "points_value": 100, "description": "The red sandstone mosque on the west side."}
    ],
    "jaipur_city_palace": [
        {"monument_id": "m_jai_1", "name": "Chandra Mahal", "points_value": 150, "description": "The seven-storey inner palace."},
        {"monument_id": "m_jai_2", "name": "Mubarak Mahal", "points_value": 100, "description": "The reception centre."}
    ],
    "goa_baga_beach": [
        {"monument_id": "m_goa_1", "name": "Aguada Fort", "points_value": 100, "description": "Historical 17th-century Portuguese fort near Baga."}
    ],
    "kerala_backwaters": [
        {"monument_id": "m_ker_1", "name": "Traditional Kettuvallam", "points_value": 50, "description": "A traditional Kerala houseboat."}
    ],
    "varanasi_ghats": [
        {"monument_id": "m_var_1", "name": "Dashashwamedh Ghat", "points_value": 150, "description": "The main and most spectacular ghat."},
        {"monument_id": "m_var_2", "name": "Kashi Vishwanath Temple", "points_value": 200, "description": "The famous Hindu temple."}
    ],
    "hampi_ruins": [
        {"monument_id": "m_ham_1", "name": "Virupaksha Temple", "points_value": 150, "description": "The main center of pilgrimage at Hampi."},
        {"monument_id": "m_ham_2", "name": "Stone Chariot", "points_value": 250, "description": "The iconic stone chariot in Vittala Temple complex."}
    ],
    "manali": [
        {"monument_id": "m_man_1", "name": "Hadimba Devi Temple", "points_value": 100, "description": "Ancient cave temple dedicated to Hidimbi Devi."}
    ],
    "mysore_palace": [
        {"monument_id": "m_mys_1", "name": "Mysore Palace Main Facade", "points_value": 150, "description": "The stunning front view of the Ambavilas Palace."}
    ]
}

# In-memory datastores
user_photo_submissions: List[Dict[str, Any]] = []
# user_id -> {"total_points": int, "points_redeemed": int, "current_balance": int}
user_points_ledger: Dict[str, Dict[str, int]] = {}

REWARD_TIERS = [
    {"tier_id": "tier_10", "points_required": 500, "discount_pct": 10, "name": "10% Off Hotel Booking"},
    {"tier_id": "tier_20", "points_required": 1000, "discount_pct": 20, "name": "20% Off Hotel Booking"},
    {"tier_id": "tier_30", "points_required": 2000, "discount_pct": 30, "name": "30% Off Hotel Booking"}
]

def init_user_ledger(user_id: str):
    if user_id not in user_points_ledger:
        user_points_ledger[user_id] = {
            "total_points": 0,
            "points_redeemed": 0,
            "current_balance": 0
        }

def get_monument(monument_id: str):
    for dest_monuments in MONUMENTS_DB.values():
        for m in dest_monuments:
            if m["monument_id"] == monument_id:
                return m
    return None
