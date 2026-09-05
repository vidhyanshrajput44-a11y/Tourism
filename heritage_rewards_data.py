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
        {"monument_id": "m_taj_2", "name": "Kau Ban Mosque", "points_value": 100, "description": "The red sandstone mosque on the west side."},
        {"monument_id": "m_taj_3", "name": "Jawab", "points_value": 100, "description": "The red sandstone guesthouse on the east side."},
        {"monument_id": "m_taj_4", "name": "Great Gate (Darwaza-i Rauza)", "points_value": 150, "description": "The spectacular main gateway to the Taj Mahal."},
        {"monument_id": "m_taj_5", "name": "Taj Museum", "points_value": 50, "description": "The museum housing Mughal artifacts within the complex."}
    ],
    "jaipur_city_palace": [
        {"monument_id": "m_jai_1", "name": "Chandra Mahal", "points_value": 150, "description": "The seven-storey inner palace with intricate decorations."},
        {"monument_id": "m_jai_2", "name": "Mubarak Mahal", "points_value": 100, "description": "The beautifully carved reception centre."},
        {"monument_id": "m_jai_3", "name": "Pritam Niwas Chowk", "points_value": 150, "description": "The courtyard with four stunning painted gateways."},
        {"monument_id": "m_jai_4", "name": "Diwan-i-Khas", "points_value": 100, "description": "The hall of private audience housing the giant silver urns."},
        {"monument_id": "m_jai_5", "name": "Diwan-i-Aam", "points_value": 100, "description": "The hall of public audience featuring miniature paintings."}
    ],
    "goa_baga_beach": [
        {"monument_id": "m_goa_1", "name": "Aguada Fort", "points_value": 150, "description": "Historical 17th-century Portuguese fort and lighthouse."},
        {"monument_id": "m_goa_2", "name": "Chapora Fort", "points_value": 150, "description": "Scenic 17th-century ruins famously featured in films."},
        {"monument_id": "m_goa_3", "name": "Basilica of Bom Jesus", "points_value": 200, "description": "UNESCO site housing the remains of St. Francis Xavier."},
        {"monument_id": "m_goa_4", "name": "Se Cathedral", "points_value": 150, "description": "One of the largest churches in Asia, known for its Golden Bell."},
        {"monument_id": "m_goa_5", "name": "Immaculate Conception Church", "points_value": 100, "description": "Iconic Panjim church with famous zigzag stairs."}
    ],
    "kerala_backwaters": [
        {"monument_id": "m_ker_1", "name": "Traditional Kettuvallam", "points_value": 100, "description": "A beautifully crafted traditional Kerala houseboat."},
        {"monument_id": "m_ker_2", "name": "Krishnapuram Palace", "points_value": 150, "description": "18th-century palace built by Anizham Thirunal Marthanda Varma."},
        {"monument_id": "m_ker_3", "name": "Alleppey Lighthouse", "points_value": 100, "description": "Historic striped coastal lighthouse built in 1862."},
        {"monument_id": "m_ker_4", "name": "Ambalappuzha Sri Krishna Temple", "points_value": 150, "description": "Ancient Hindu temple famous for its Palpayasam."},
        {"monument_id": "m_ker_5", "name": "St. Andrew's Basilica", "points_value": 100, "description": "Historic 16th-century coastal church."}
    ],
    "varanasi_ghats": [
        {"monument_id": "m_var_1", "name": "Dashashwamedh Ghat", "points_value": 150, "description": "The main and most spectacular ghat, site of Ganga Aarti."},
        {"monument_id": "m_var_2", "name": "Kashi Vishwanath Temple", "points_value": 200, "description": "One of the most famous Hindu temples dedicated to Lord Shiva."},
        {"monument_id": "m_var_3", "name": "Manikarnika Ghat", "points_value": 150, "description": "The ancient and sacred cremation ghat on the Ganges."},
        {"monument_id": "m_var_4", "name": "Ramnagar Fort", "points_value": 100, "description": "The sandstone fort and museum of the Kashi Naresh."},
        {"monument_id": "m_var_5", "name": "Assi Ghat", "points_value": 100, "description": "The southernmost ghat, traditionally visited by pilgrims first."}
    ],
    "hampi_ruins": [
        {"monument_id": "m_ham_1", "name": "Virupaksha Temple", "points_value": 150, "description": "The main center of pilgrimage with a towering gopuram."},
        {"monument_id": "m_ham_2", "name": "Stone Chariot", "points_value": 200, "description": "The iconic and intricately carved stone chariot."},
        {"monument_id": "m_ham_3", "name": "Vittala Temple", "points_value": 150, "description": "The architectural showpiece of Hampi (musical pillars)."},
        {"monument_id": "m_ham_4", "name": "Lotus Mahal", "points_value": 100, "description": "An elegant, lotus-like pavilion in the Zenana Enclosure."},
        {"monument_id": "m_ham_5", "name": "Elephant Stables", "points_value": 100, "description": "The grand domed structure used to house royal elephants."}
    ],
    "manali": [
        {"monument_id": "m_man_1", "name": "Hadimba Devi Temple", "points_value": 150, "description": "Ancient wooden cave temple surrounded by cedar forests."},
        {"monument_id": "m_man_2", "name": "Manu Temple", "points_value": 100, "description": "Historic temple dedicated to sage Manu in Old Manali."},
        {"monument_id": "m_man_3", "name": "Vashisht Temple", "points_value": 100, "description": "Traditional temples featuring natural geothermal hot springs."},
        {"monument_id": "m_man_4", "name": "Naggar Castle", "points_value": 150, "description": "A magnificent historic castle blending Himalayan/European architecture."},
        {"monument_id": "m_man_5", "name": "Nicholas Roerich Art Gallery", "points_value": 100, "description": "The heritage home and gallery of the famous Russian artist."}
    ],
    "mysore_palace": [
        {"monument_id": "m_mys_1", "name": "Ambavilas Palace Facade", "points_value": 200, "description": "The stunning, illuminated front view of the main Mysore Palace."},
        {"monument_id": "m_mys_2", "name": "Jaganmohan Palace", "points_value": 150, "description": "Traditional palace now housing a magnificent art gallery."},
        {"monument_id": "m_mys_3", "name": "Chamundeshwari Temple", "points_value": 150, "description": "The ancient hilltop temple overlooking Mysore."},
        {"monument_id": "m_mys_4", "name": "Nandi Statue (Bull Temple)", "points_value": 100, "description": "The massive monolithic Nandi carved out of a single boulder."},
        {"monument_id": "m_mys_5", "name": "St. Philomena's Cathedral", "points_value": 100, "description": "A towering neo-Gothic church built in 1936."}
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
