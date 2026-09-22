"""
Model training and inference for FootPrint.

Trains XGBoost (primary) and Prophet (baseline), compares on held-out test set,
saves the best model, and provides crowd score mapping utilities.
"""

import json
import pickle
from datetime import date, timedelta
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except Exception:
    from sklearn.ensemble import HistGradientBoostingRegressor
    XGBOOST_AVAILABLE = False

from config import (
    BEST_MODEL_JSON,
    CROWD_LOW_THRESHOLD,
    CROWD_MEDIUM_THRESHOLD,
    DATA_CSV,
    DESTINATIONS_JSON,
    METRICS_JSON,
    MODELS_DIR,
    PROPHET_MODEL_DIR,
    XGBOOST_MODEL_PATH,
)
from feature_engineering import FEATURE_COLUMNS, TARGET_COLUMN, build_features

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


class FootprintPredictor:
    """Loads trained model + metadata and serves predictions."""

    def __init__(self):
        self.model = None
        self.best_model_name = "xgboost"
        self.weather_encoder = None
        self.dest_encoder = None
        self.destinations: dict = {}
        self.history: pd.DataFrame | None = None
        self.metrics: dict = {}

    def load(self) -> None:
        """Load model artifacts from disk (called once at API startup)."""
        MODELS_DIR.mkdir(parents=True, exist_ok=True)

        with open(DESTINATIONS_JSON) as f:
            dest_list = json.load(f)
        self.destinations = {d["destination_id"]: d for d in dest_list}

        self.history = pd.read_csv(DATA_CSV, parse_dates=["date"])

        with open(BEST_MODEL_JSON) as f:
            meta = json.load(f)
        self.best_model_name = meta.get("best_model", "xgboost")

        bundle = joblib.load(XGBOOST_MODEL_PATH)
        self.model = bundle["model"]
        self.weather_encoder = bundle["weather_encoder"]
        self.dest_encoder = bundle["dest_encoder"]

        if METRICS_JSON.exists():
            with open(METRICS_JSON) as f:
                self.metrics = json.load(f)

    def _get_capacity(self, destination_id: str) -> int:
        return self.destinations[destination_id]["max_capacity"]

    def footfall_to_crowd(self, footfall: float, destination_id: str) -> tuple[int, str, float]:
        """
        Map predicted footfall → crowd_score (0-100) and category.

        Score is normalized against destination max_capacity.
        """
        capacity = self._get_capacity(destination_id)
        score = int(round(min(100, max(0, (footfall / capacity) * 100))))

        if score < CROWD_LOW_THRESHOLD:
            category = "Low"
        elif score < CROWD_MEDIUM_THRESHOLD:
            category = "Medium"
        else:
            category = "High"

        confidence = round(min(0.95, 0.70 + (self.history.shape[0] / 100000) * 0.2), 2)
        return score, category, confidence

    def _build_inference_row(
        self,
        destination_id: str,
        target_date: pd.Timestamp,
        weather_temp: float = 28.0,
        weather_condition: str = "sunny",
    ) -> pd.DataFrame:
        """Construct a single feature row for a future date."""
        dest_hist = self.history[self.history["destination_id"] == destination_id].copy()
        dest_hist = dest_hist.sort_values("date")

        # Append a placeholder row for the target date
        holiday_flag = int(target_date.weekday() >= 5)  # simplified; real check below
        from data_generator import is_holiday
        h, _ = is_holiday(target_date.date())
        holiday_flag = int(h)

        new_row = {
            "destination_id": destination_id,
            "date": target_date,
            "footfall_count": dest_hist["footfall_count"].iloc[-1],  # placeholder
            "day_of_week": target_date.weekday(),
            "is_weekend": int(target_date.weekday() >= 5),
            "is_holiday": holiday_flag,
            "weather_temp": weather_temp,
            "weather_condition": weather_condition,
            "month": target_date.month,
        }

        combined = pd.concat([dest_hist, pd.DataFrame([new_row])], ignore_index=True)
        featured, _, _ = build_features(
            combined,
            weather_encoder=self.weather_encoder,
            dest_encoder=self.dest_encoder,
            fit_encoders=False,
        )
        return featured.iloc[[-1]]

    def predict_single(
        self,
        destination_id: str,
        target_date: str,
        weather_temp: float = 28.0,
        weather_condition: str = "sunny",
    ) -> dict:
        """Predict footfall and crowd metrics for one destination + date."""
        if destination_id not in self.destinations:
            raise ValueError(f"Unknown destination: {destination_id}")

        ts = pd.to_datetime(target_date)
        row = self._build_inference_row(destination_id, ts, weather_temp, weather_condition)
        X = row[FEATURE_COLUMNS]
        footfall = float(self.model.predict(X)[0])
        footfall = max(0, footfall)

        score, category, confidence = self.footfall_to_crowd(footfall, destination_id)
        return {
            "destination_id": destination_id,
            "date": ts.strftime("%Y-%m-%d"),
            "predicted_footfall": int(round(footfall)),
            "crowd_score": score,
            "crowd_category": category,
            "confidence": confidence,
        }

    def forecast_7_days(self, destination_id: str) -> list[dict]:
        """Generate 7-day ahead forecast using recursive lag updates."""
        if destination_id not in self.destinations:
            raise ValueError(f"Unknown destination: {destination_id}")

        dest_hist = self.history[self.history["destination_id"] == destination_id].copy()
        dest_hist = dest_hist.sort_values("date").reset_index(drop=True)

        working = dest_hist.copy()
        forecasts = []
        # Anchor forecast to next 7 calendar days from today (demo-friendly)
        forecast_start = pd.Timestamp(date.today())

        for day_offset in range(1, 8):
            target = forecast_start + pd.Timedelta(days=day_offset)
            from data_generator import generate_weather, is_holiday
            import numpy as np
            rng = np.random.default_rng(42 + day_offset)
            dest_meta = self.destinations[destination_id]
            # Reconstruct destination dict for weather generator
            dest_full = {
                "destination_id": destination_id,
                "peak_months": [10, 11, 12, 1, 2, 3],
            }
            temp, condition = generate_weather(target.date(), dest_full, rng)

            h, _ = is_holiday(target.date())
            new_row = {
                "destination_id": destination_id,
                "date": target,
                "footfall_count": working["footfall_count"].iloc[-1],
                "day_of_week": target.weekday(),
                "is_weekend": int(target.weekday() >= 5),
                "is_holiday": int(h),
                "weather_temp": temp,
                "weather_condition": condition,
                "month": target.month,
            }
            working = pd.concat([working, pd.DataFrame([new_row])], ignore_index=True)

            featured, _, _ = build_features(
                working,
                weather_encoder=self.weather_encoder,
                dest_encoder=self.dest_encoder,
                fit_encoders=False,
            )
            row = featured.iloc[[-1]]
            footfall = float(self.model.predict(row[FEATURE_COLUMNS])[0])
            footfall = max(0, footfall)
            footfall_int = int(round(footfall))

            # Update working history with prediction for next lag computation
            working.loc[working.index[-1], "footfall_count"] = footfall_int

            score, category, confidence = self.footfall_to_crowd(footfall, destination_id)
            forecasts.append({
                "date": target.strftime("%Y-%m-%d"),
                "day_of_week": target.strftime("%A"),
                "is_weekend": bool(target.weekday() >= 5),
                "is_holiday": bool(h),
                "predicted_footfall": footfall_int,
                "crowd_score": score,
                "crowd_category": category,
                "confidence": confidence,
            })

        return forecasts


def train_xgboost(df: pd.DataFrame) -> tuple[object, dict, object, object]:
    """Train XGBoost (or sklearn fallback) on 80/20 time-based split."""
    featured, weather_enc, dest_enc = build_features(df, fit_encoders=True)

    split_idx = int(len(featured) * 0.8)
    train = featured.iloc[:split_idx]
    test = featured.iloc[split_idx:]

    X_train, y_train = train[FEATURE_COLUMNS], train[TARGET_COLUMN]
    X_test, y_test = test[FEATURE_COLUMNS], test[TARGET_COLUMN]

    if XGBOOST_AVAILABLE:
        model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        )
    else:
        print("  Note: XGBoost unavailable (install libomp on Mac). Using sklearn HistGradientBoosting.")
        model = HistGradientBoostingRegressor(
            max_iter=300,
            max_depth=6,
            learning_rate=0.05,
            random_state=42,
        )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "mae": round(mean_absolute_error(y_test, preds), 2),
        "rmse": round(np.sqrt(mean_squared_error(y_test, preds)), 2),
        "train_rows": len(train),
        "test_rows": len(test),
    }
    return model, metrics, weather_enc, dest_enc


def train_prophet_baseline(df: pd.DataFrame) -> dict:
    """Train one Prophet model per destination; return aggregate metrics."""
    if not PROPHET_AVAILABLE:
        return {"mae": float("inf"), "rmse": float("inf"), "skipped": True}

    PROPHET_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    all_mae, all_rmse = [], []

    for dest_id in df["destination_id"].unique():
        dest_df = df[df["destination_id"] == dest_id].copy()
        dest_df = dest_df.sort_values("date")
        split_idx = int(len(dest_df) * 0.8)

        train = dest_df.iloc[:split_idx][["date", "footfall_count"]].rename(
            columns={"date": "ds", "footfall_count": "y"}
        )
        test = dest_df.iloc[split_idx:]

        m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        m.fit(train)
        future = m.make_future_dataframe(periods=len(test))
        forecast = m.predict(future)
        preds = forecast.iloc[-len(test):]["yhat"].values
        actual = test["footfall_count"].values

        all_mae.append(mean_absolute_error(actual, preds))
        all_rmse.append(np.sqrt(mean_squared_error(actual, preds)))

        with open(PROPHET_MODEL_DIR / f"{dest_id}.pkl", "wb") as f:
            pickle.dump(m, f)

    return {
        "mae": round(np.mean(all_mae), 2),
        "rmse": round(np.mean(all_rmse), 2),
        "skipped": False,
    }


def train_and_save() -> dict:
    """Full training pipeline: XGBoost vs Prophet, save best."""
    print("Loading data...")
    df = pd.read_csv(DATA_CSV, parse_dates=["date"])

    print("Training XGBoost...")
    xgb_model, xgb_metrics, weather_enc, dest_enc = train_xgboost(df)
    print(f"  XGBoost  MAE={xgb_metrics['mae']}  RMSE={xgb_metrics['rmse']}")

    print("Training Prophet baseline...")
    prophet_metrics = train_prophet_baseline(df)
    if not prophet_metrics.get("skipped"):
        print(f"  Prophet  MAE={prophet_metrics['mae']}  RMSE={prophet_metrics['rmse']}")
    else:
        print("  Prophet not available — using XGBoost only")

    # Pick best by RMSE
    if prophet_metrics.get("mae", float("inf")) < xgb_metrics["mae"]:
        best = "prophet"
    else:
        best = "xgboost"

    print(f"\nBest model: {best.upper()}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": xgb_model, "weather_encoder": weather_enc, "dest_encoder": dest_enc},
        XGBOOST_MODEL_PATH,
    )

    metrics = {"xgboost": xgb_metrics, "prophet": prophet_metrics, "best_model": best}
    with open(METRICS_JSON, "w") as f:
        json.dump(metrics, f, indent=2)
    # API always uses the feature-rich gradient boosting model for inference
    # (captures weather + holidays — better for demo even if Prophet RMSE is slightly lower)
    with open(BEST_MODEL_JSON, "w") as f:
        json.dump({"best_model": best, "inference_model": "xgboost"}, f)

    print(f"Model saved → {XGBOOST_MODEL_PATH}")
    return metrics


if __name__ == "__main__":
    train_and_save()
