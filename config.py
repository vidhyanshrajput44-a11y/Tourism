"""Shared configuration for FootPrint crowd forecasting."""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

DATA_CSV = DATA_DIR / "footfall_history.csv"
DESTINATIONS_JSON = DATA_DIR / "destinations.json"
XGBOOST_MODEL_PATH = MODELS_DIR / "xgboost_footfall_model.joblib"
PROPHET_MODEL_DIR = MODELS_DIR / "prophet_models"
METRICS_JSON = MODELS_DIR / "model_metrics.json"
BEST_MODEL_JSON = MODELS_DIR / "best_model.json"

# Crowd score thresholds (percentage of destination max capacity)
CROWD_LOW_THRESHOLD = 40
CROWD_MEDIUM_THRESHOLD = 70

# Forecast horizon
FORECAST_DAYS = 7
