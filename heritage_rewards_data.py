"""
Data layer for UI 8 - Photo-Based Heritage Rewards + Booking Redemption.
"""

from typing import List, Dict, Any
from datetime import datetime
import uuid

# Define monuments for each destination (reusing UI 1 destination IDs)
MONUMENTS_DB = {
    "taj_mahal": [
        {"monument_id": "m_taj_1", "name": "Taj Mahal Main Mausoleum", "points_value": 200, "description": "The central white marble structure.", "image_url": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_taj_2", "name": "Kau Ban Mosque", "points_value": 100, "description": "The red sandstone mosque on the west side.", "image_url": "https://images.unsplash.com/photo-1585135497273-1a86b09fe70e?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_taj_3", "name": "Jawab", "points_value": 100, "description": "The red sandstone guesthouse on the east side.", "image_url": "https://images.unsplash.com/photo-1598890777032-bde13fbe3492?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_taj_4", "name": "Great Gate (Darwaza-i Rauza)", "points_value": 150, "description": "The spectacular main gateway to the Taj Mahal.", "image_url": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_taj_5", "name": "Taj Museum", "points_value": 50, "description": "The museum housing Mughal artifacts within the complex.", "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=800&q=80"}
    ],
    "jaipur_city_palace": [
        {"monument_id": "m_jai_1", "name": "Chandra Mahal", "points_value": 150, "description": "The seven-storey inner palace with intricate decorations.", "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_jai_2", "name": "Mubarak Mahal", "points_value": 100, "description": "The beautifully carved reception centre.", "image_url": "https://images.unsplash.com/photo-1609137144822-2936952d7658?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_jai_3", "name": "Pritam Niwas Chowk", "points_value": 150, "description": "The courtyard with four stunning painted gateways.", "image_url": "https://images.unsplash.com/photo-1757310062384-d3bcfe3026e8?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_jai_4", "name": "Diwan-i-Khas", "points_value": 100, "description": "The hall of private audience housing the giant silver urns.", "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_jai_5", "name": "Diwan-i-Aam", "points_value": 100, "description": "The hall of public audience featuring miniature paintings.", "image_url": "https://images.unsplash.com/photo-1600100397608-f010e4277c08?auto=format&fit=crop&w=800&q=80"}
    ],
    "goa_baga_beach": [
        {"monument_id": "m_goa_1", "name": "Aguada Fort", "points_value": 150, "description": "Historical 17th-century Portuguese fort and lighthouse.", "image_url": "https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_goa_2", "name": "Chapora Fort", "points_value": 150, "description": "Scenic 17th-century ruins famously featured in films.", "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_goa_3", "name": "Basilica of Bom Jesus", "points_value": 200, "description": "UNESCO site housing the remains of St. Francis Xavier.", "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_goa_4", "name": "Se Cathedral", "points_value": 150, "description": "One of the largest churches in Asia, known for its Golden Bell.", "image_url": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_goa_5", "name": "Immaculate Conception Church", "points_value": 100, "description": "Iconic Panjim church with famous zigzag stairs.", "image_url": "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=800&q=80"}
    ],
    "kerala_backwaters": [
        {"monument_id": "m_ker_1", "name": "Traditional Kettuvallam", "points_value": 100, "description": "A beautifully crafted traditional Kerala houseboat.", "image_url": "https://images.unsplash.com/photo-1593693401060-9fc28cf9e368?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ker_2", "name": "Krishnapuram Palace", "points_value": 150, "description": "18th-century palace built by Anizham Thirunal Marthanda Varma.", "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ker_3", "name": "Alleppey Lighthouse", "points_value": 100, "description": "Historic striped coastal lighthouse built in 1862.", "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ker_4", "name": "Ambalappuzha Sri Krishna Temple", "points_value": 150, "description": "Ancient Hindu temple famous for its Palpayasam.", "image_url": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ker_5", "name": "St. Andrew's Basilica", "points_value": 100, "description": "Historic 16th-century coastal church.", "image_url": "https://images.unsplash.com/photo-1548625361-19597793d987?auto=format&fit=crop&w=800&q=80"}
    ],
    "varanasi_ghats": [
        {"monument_id": "m_var_1", "name": "Dashashwamedh Ghat", "points_value": 150, "description": "The main and most spectacular ghat, site of Ganga Aarti.", "image_url": "https://images.unsplash.com/photo-1561359313-0639aad073f0?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_var_2", "name": "Kashi Vishwanath Temple", "points_value": 200, "description": "One of the most famous Hindu temples dedicated to Lord Shiva.", "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_var_3", "name": "Manikarnika Ghat", "points_value": 150, "description": "The ancient and sacred cremation ghat on the Ganges.", "image_url": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_var_4", "name": "Ramnagar Fort", "points_value": 100, "description": "The sandstone fort and museum of the Kashi Naresh.", "image_url": "https://images.unsplash.com/photo-1627894483216-2138af692e32?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_var_5", "name": "Assi Ghat", "points_value": 100, "description": "The southernmost ghat, traditionally visited by pilgrims first.", "image_url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71?auto=format&fit=crop&w=800&q=80"}
    ],
    "hampi_ruins": [
        {"monument_id": "m_ham_1", "name": "Virupaksha Temple", "points_value": 150, "description": "The main center of pilgrimage with a towering gopuram.", "image_url": "https://images.unsplash.com/photo-1600100397608-f010e4277c08?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ham_2", "name": "Stone Chariot", "points_value": 200, "description": "The iconic and intricately carved stone chariot.", "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ham_3", "name": "Vittala Temple", "points_value": 150, "description": "The architectural showpiece of Hampi (musical pillars).", "image_url": "https://images.unsplash.com/photo-1722934804353-0d9f6a55ab5e?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ham_4", "name": "Lotus Mahal", "points_value": 100, "description": "An elegant, lotus-like pavilion in the Zenana Enclosure.", "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_ham_5", "name": "Elephant Stables", "points_value": 100, "description": "The grand domed structure used to house royal elephants.", "image_url": "https://images.unsplash.com/photo-1598890777032-bde13fbe3492?auto=format&fit=crop&w=800&q=80"}
    ],
    "manali": [
        {"monument_id": "m_man_1", "name": "Hadimba Devi Temple", "points_value": 150, "description": "Ancient wooden cave temple surrounded by cedar forests.", "image_url": "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_man_2", "name": "Manu Temple", "points_value": 100, "description": "Historic temple dedicated to sage Manu in Old Manali.", "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_man_3", "name": "Vashisht Temple", "points_value": 100, "description": "Traditional temples featuring natural geothermal hot springs.", "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_man_4", "name": "Naggar Castle", "points_value": 150, "description": "A magnificent historic castle blending Himalayan/European architecture.", "image_url": "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_man_5", "name": "Nicholas Roerich Art Gallery", "points_value": 100, "description": "The heritage home and gallery of the famous Russian artist.", "image_url": "https://images.unsplash.com/photo-1517824806704-9040b037703b?auto=format&fit=crop&w=800&q=80"}
    ],
    "mysore_palace": [
        {"monument_id": "m_mys_1", "name": "Ambavilas Palace Facade", "points_value": 200, "description": "The stunning, illuminated front view of the main Mysore Palace.", "image_url": "https://images.unsplash.com/photo-1611510338559-2f463335092c?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_mys_2", "name": "Jaganmohan Palace", "points_value": 150, "description": "Traditional palace now housing a magnificent art gallery.", "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_mys_3", "name": "Chamundeshwari Temple", "points_value": 150, "description": "The ancient hilltop temple overlooking Mysore.", "image_url": "https://images.unsplash.com/photo-1600100397608-f010e4277c08?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_mys_4", "name": "Nandi Statue (Bull Temple)", "points_value": 100, "description": "The massive monolithic Nandi carved out of a single boulder.", "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80"},
        {"monument_id": "m_mys_5", "name": "St. Philomena's Cathedral", "points_value": 100, "description": "A towering neo-Gothic church built in 1936.", "image_url": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80"}
    ],
    "kempty_falls": [
        {"monument_id": "m_kem_1", "name": "Upper Kempty Waterfall", "points_value": 150, "description": "Iconic cascading mountain stream and plunge pool.", "image_url": "images/kempty_falls.jpg"},
        {"monument_id": "m_kem_2", "name": "Mussoorie Ropeway Point", "points_value": 100, "description": "Scenic cable car lookout facing the lower Himalayan ranges.", "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"}
    ],
    "robbers_cave": [
        {"monument_id": "m_rob_1", "name": "Guchhupani Natural Limestone Gorge", "points_value": 150, "description": "Fascinating natural narrow limestone formation with knee-deep cold streams.", "image_url": "images/robbers_cave.jpg"},
        {"monument_id": "m_rob_2", "name": "Subterranean Stream Cave Walk", "points_value": 100, "description": "Hidden underground river path tucked inside the scenic Doon valley.", "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=800&q=80"}
    ]
}

# In-memory datastores
user_photo_submissions: List[Dict[str, Any]] = []
# user_id -> {"total_points": int, "points_redeemed": int, "current_balance": int}
user_points_ledger: Dict[str, Dict[str, int]] = {}

REWARD_TIERS = [
    {"tier_id": "tier_1", "points_required": 50, "discount_pct": 1, "name": "1% Off Hotel Booking"},
    {"tier_id": "tier_5", "points_required": 150, "discount_pct": 5, "name": "5% Off Hotel Booking"},
    {"tier_id": "tier_10", "points_required": 300, "discount_pct": 10, "name": "10% Off Hotel Booking (Max)"}
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
