"""
FastAPI server for FootPrint Predictive Crowd Intelligence.

Endpoints:
  POST /predict              → single date prediction
  GET  /forecast/{dest_id}   → 7-day forecast array
  GET  /destinations         → all destinations with today's crowd category
  GET  /health               → health check
"""

from contextlib import asynccontextmanager
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from model import FootprintPredictor

FRONTEND_DIR = Path(__file__).parent / "frontend"

predictor = FootprintPredictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model once at startup — not on every request."""
    predictor.load()
    try:
        list_destinations()
    except Exception:
        pass
    yield


app = FastAPI(
    title="FootPrint — Predictive Crowd Intelligence",
    description="AI-powered tourism crowd forecasting for Smart India Hackathon 2026",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class PredictRequest(BaseModel):
    destination_id: str = Field(..., examples=["taj_mahal"])
    date: str = Field(..., examples=["2026-09-10"])
    weather_temp: float | None = Field(None, ge=-10, le=50)
    weather_condition: str | None = Field(None, examples=["sunny"])

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            parsed = date.fromisoformat(v)
        except ValueError:
            raise ValueError("date must be ISO format YYYY-MM-DD")
        if parsed < date.today():
            raise ValueError("date must be today or in the future")
        if parsed > date.today() + timedelta(days=30):
            raise ValueError("date must be within 30 days from today")
        return v


class PredictResponse(BaseModel):
    destination_id: str
    date: str
    predicted_footfall: int
    crowd_score: int
    crowd_category: str
    confidence: float


class ForecastDay(BaseModel):
    date: str
    day_of_week: str
    is_weekend: bool
    is_holiday: bool
    predicted_footfall: int
    crowd_score: int
    crowd_category: str
    confidence: float


class DestinationInfo(BaseModel):
    destination_id: str
    name: str
    city: str
    state: str
    max_capacity: int
    current_crowd_category: str
    current_crowd_score: int


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "inference_model": "xgboost",
        "best_on_test_set": predictor.best_model_name,
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        result = predictor.predict_single(
            req.destination_id,
            req.date,
            weather_temp=req.weather_temp or 28.0,
            weather_condition=req.weather_condition or "sunny",
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


_destinations_cache = None
_destinations_cache_date = None
_forecast_cache = {}


@app.get("/forecast/{destination_id}", response_model=list[ForecastDay])
def forecast(destination_id: str):
    today = date.today().isoformat()
    cache_key = (destination_id, today)
    if cache_key in _forecast_cache:
        return _forecast_cache[cache_key]
    try:
        data = predictor.forecast_7_days(destination_id)
        _forecast_cache[cache_key] = data
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast failed: {e}")


@app.get("/destinations", response_model=list[DestinationInfo])
def list_destinations():
    global _destinations_cache, _destinations_cache_date
    today = date.today().isoformat()
    if _destinations_cache is not None and _destinations_cache_date == today:
        return _destinations_cache

    results = []
    for dest_id, meta in predictor.destinations.items():
        try:
            pred = predictor.predict_single(dest_id, today)
            category = pred["crowd_category"]
            score = pred["crowd_score"]
        except Exception:
            category, score = "Medium", 50

        results.append(DestinationInfo(
            destination_id=dest_id,
            name=meta["name"],
            city=meta["city"],
            state=meta["state"],
            max_capacity=meta["max_capacity"],
            current_crowd_category=category,
            current_crowd_score=score,
        ))
    _destinations_cache = results
    _destinations_cache_date = today
    return results

# --- UI 2: AI Crowd Redistribution Engine (Added without breaking UI 1) ---
from recommend_api import recommend_router
app.include_router(recommend_router)

# --- UI 3: Smart Safety + Emergency SOS Engine (Added without breaking UI 1 or UI 2) ---
from safety_api import safety_router
app.include_router(safety_router)

# --- UI 4: Local Market Connect + Hidden Gems (Added without breaking UI 1, 2, or 3) ---
from local_market_api import local_router
app.include_router(local_router)

# --- UI 5: Government Dashboard + Crowd Vision ---
from gov_dashboard_api import gov_router
app.include_router(gov_router)

# --- UI 6: Hotel Demand & Transport Routing ---
from hotel_transport_api import ht_router
app.include_router(ht_router)

# --- UI 7: RAG Chatbot ---
from chatbot_api import chat_router
app.include_router(chat_router)

# --- UI 8: Authentication ---
from auth_api import auth_router
app.include_router(auth_router)
# ---------------------------------------------------------------------------

# --- UI 9: Photo-Based Heritage Rewards ---
from heritage_rewards_api import rewards_router
app.include_router(rewards_router)
# ---------------------------------------------------------------------------

# Serve frontend (must be after API routes)
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
