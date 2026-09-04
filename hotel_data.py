import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import httpx
import os
import json

with open("hotels_db_dump.json", "r") as f:
    HOTELS_DB = json.load(f)

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
