import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from datetime import datetime, timedelta
import os

MODEL_PATH = "hotel_model.pkl"

def engineer_features(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['hotel_id', 'date'])
    
    # Lag features
    df['occ_lag_1'] = df.groupby('hotel_id')['occupancy_pct'].shift(1)
    df['occ_lag_7'] = df.groupby('hotel_id')['occupancy_pct'].shift(7)
    
    # Rolling averages
    df['occ_rolling_7'] = df.groupby('hotel_id')['occupancy_pct'].transform(lambda x: x.rolling(7).mean())
    
    # Fill NAs
    df.bfill(inplace=True)
    return df

def train_model():
    print("Training Hotel Demand Model...")
    df = pd.read_csv("hotel_synthetic_data.csv")
    df = engineer_features(df)
    
    features = ['day_of_week', 'is_weekend', 'is_holiday', 'occ_lag_1', 'occ_lag_7', 'occ_rolling_7']
    X = df[features]
    y = df['occupancy_pct']
    
    model = HistGradientBoostingRegressor(learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

def load_or_train():
    if not os.path.exists(MODEL_PATH):
        if not os.path.exists("hotel_synthetic_data.csv"):
            import hotel_data
            hotel_data.generate_hotel_training_data()
        train_model()
    
    return joblib.load(MODEL_PATH)

# Global model instance
model = load_or_train()
df_hist = engineer_features(pd.read_csv("hotel_synthetic_data.csv"))

def predict_occupancy(hotel_id: str, days: int = 7):
    hotel_hist = df_hist[df_hist['hotel_id'] == hotel_id].copy()
    if hotel_hist.empty:
        return []
        
    last_row = hotel_hist.iloc[-1]
    current_date = pd.to_datetime(last_row['date'])
    
    hist_occ = list(hotel_hist['occupancy_pct'])
    
    forecasts = []
    
    for i in range(1, days + 1):
        target_date = current_date + timedelta(days=i)
        dow = target_date.weekday()
        is_weekend = 1 if dow >= 5 else 0
        is_hol = 1 if target_date.strftime("%m-%d") in ["01-26", "08-15", "10-02", "12-25", "12-31", "01-01", "10-24", "11-12", "03-08"] else 0
        
        lag_1 = hist_occ[-1]
        lag_7 = hist_occ[-7] if len(hist_occ) >= 7 else np.mean(hist_occ)
        roll_7 = np.mean(hist_occ[-7:]) if len(hist_occ) >= 7 else np.mean(hist_occ)
        
        features = pd.DataFrame([{
            'day_of_week': dow,
            'is_weekend': is_weekend,
            'is_holiday': is_hol,
            'occ_lag_1': lag_1,
            'occ_lag_7': lag_7,
            'occ_rolling_7': roll_7
        }])
        
        pred_occ = float(model.predict(features)[0])
        pred_occ = max(0.0, min(100.0, pred_occ))
        
        demand_cat = "Low" if pred_occ < 50 else "Medium" if pred_occ < 80 else "High"
        
        pricing_sug = ""
        if demand_cat == "High":
            pricing_sug = "High demand — consider +15% pricing"
        elif demand_cat == "Low":
            pricing_sug = "Low demand — consider promotional pricing"
        else:
            pricing_sug = "Stable demand — standard pricing"
            
        forecasts.append({
            "date": target_date.strftime("%Y-%m-%d"),
            "occupancy_pct": round(pred_occ, 1),
            "demand_category": demand_cat,
            "pricing_suggestion": pricing_sug
        })
        
        hist_occ.append(pred_occ)
        
    return forecasts

if __name__ == "__main__":
    load_or_train()
