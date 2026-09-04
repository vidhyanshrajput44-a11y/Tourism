import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import httpx
import os

# Base hotels mapping
HOTELS_DB = {
    "taj_mahal": [
        {"hotel_id": "h_taj_1", "name": "The Oberoi Amarvilas", "star_rating": 5.0, "total_rooms": 102, "base_price": 45000},
        {"hotel_id": "h_taj_2", "name": "Taj Hotel & Convention", "star_rating": 5.0, "total_rooms": 239, "base_price": 12000},
        {"hotel_id": "h_taj_3", "name": "Joey's Hostel Agra", "star_rating": 3.0, "total_rooms": 45, "base_price": 800}
    ],
    "jaipur_city_palace": [
        {"hotel_id": "h_jai_1", "name": "Rambagh Palace", "star_rating": 5.0, "total_rooms": 78, "base_price": 55000},
        {"hotel_id": "h_jai_2", "name": "Zostel Jaipur", "star_rating": 3.5, "total_rooms": 60, "base_price": 1100}
    ],
    "goa_baga_beach": [
        {"hotel_id": "h_goa_1", "name": "Taj Holiday Village", "star_rating": 5.0, "total_rooms": 142, "base_price": 18000},
        {"hotel_id": "h_goa_2", "name": "Baga Beach Resort", "star_rating": 4.0, "total_rooms": 80, "base_price": 6000},
        {"hotel_id": "h_goa_3", "name": "HostelCrowd Goa", "star_rating": 3.0, "total_rooms": 120, "base_price": 900}
    ],
    "kerala_backwaters": [
        {"hotel_id": "h_ker_1", "name": "Kumarakom Lake Resort", "star_rating": 5.0, "total_rooms": 59, "base_price": 25000},
        {"hotel_id": "h_ker_2", "name": "Alleppey Houseboat Stays", "star_rating": 4.0, "total_rooms": 20, "base_price": 8000}
    ],
    "varanasi_ghats": [
        {"hotel_id": "h_var_1", "name": "BrijRama Palace", "star_rating": 5.0, "total_rooms": 32, "base_price": 22000},
        {"hotel_id": "h_var_2", "name": "Ganges Inn", "star_rating": 3.0, "total_rooms": 40, "base_price": 2500}
    ],
    "hampi_ruins": [
        {"hotel_id": "h_ham_1", "name": "Evolve Back Hampi", "star_rating": 5.0, "total_rooms": 46, "base_price": 30000},
        {"hotel_id": "h_ham_2", "name": "Heritage Resort Hampi", "star_rating": 4.0, "total_rooms": 50, "base_price": 8000}
    ],
    "manali": [
        {"hotel_id": "h_man_1", "name": "Span Resort & Spa", "star_rating": 5.0, "total_rooms": 36, "base_price": 15000},
        {"hotel_id": "h_man_2", "name": "Zostel Manali", "star_rating": 3.0, "total_rooms": 70, "base_price": 1000}
    ],
    "mysore_palace": [
        {"hotel_id": "h_mys_1", "name": "Lalitha Mahal Palace", "star_rating": 4.5, "total_rooms": 54, "base_price": 9000},
        {"hotel_id": "h_mys_2", "name": "Southern Star Mysore", "star_rating": 4.0, "total_rooms": 105, "base_price": 5000}
    ]
}

def generate_hotel_training_data():
    """Generates ~1 year of synthetic daily occupancy data per hotel."""
    data = []
    start_date = datetime.today() - timedelta(days=365)
    
    # Simple Indian holidays approximation (same heuristic as UI 1)
    holidays = [
        "01-26", "08-15", "10-02", "12-25", "12-31", "01-01",
        "10-24", "11-12", "03-08" 
    ]
    
    for dest_id, hotels in HOTELS_DB.items():
        for h in hotels:
            base_occ = 40 + (h["star_rating"] * 5) # Higher star, slightly higher baseline
            for i in range(365):
                dt = start_date + timedelta(days=i)
                day_of_week = dt.weekday()
                is_weekend = 1 if day_of_week >= 5 else 0
                is_holiday = 1 if dt.strftime("%m-%d") in holidays else 0
                
                # Seasonality: higher in winter (Nov-Feb), lower in summer/monsoon
                month = dt.month
                season_mult = 1.3 if month in [11,12,1,2] else 0.8 if month in [4,5,6,7] else 1.0
                
                # Calculate occupancy
                occ = base_occ * season_mult
                if is_weekend:
                    occ += 15
                if is_holiday:
                    occ += 25
                
                # Add noise
                occ += random.uniform(-10, 10)
                occ = max(10, min(100, occ)) # Cap between 10% and 100%
                
                # Dynamic pricing based on occupancy
                price_mult = 1.0
                if occ > 85:
                    price_mult = 1.2
                elif occ < 40:
                    price_mult = 0.8
                    
                data.append({
                    "hotel_id": h["hotel_id"],
                    "destination_id": dest_id,
                    "date": dt.strftime("%Y-%m-%d"),
                    "day_of_week": day_of_week,
                    "is_weekend": is_weekend,
                    "is_holiday": is_holiday,
                    "occupancy_pct": round(occ, 1),
                    "avg_price_that_night": round(h["base_price"] * price_mult)
                })
                
    df = pd.DataFrame(data)
    df.to_csv("hotel_synthetic_data.csv", index=False)
    print("Generated hotel_synthetic_data.csv")

if __name__ == "__main__":
    if not os.path.exists("hotel_synthetic_data.csv"):
        generate_hotel_training_data()
