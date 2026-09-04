from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from recommender import CrowdRecommender
from destination_metadata import get_metadata_or_raise

# Router for UI 2 — AI Crowd Redistribution / Recommendation Engine
recommend_router = APIRouter(prefix="/ui2", tags=["UI 2 - Recommendations"])

recommender = CrowdRecommender()

class AlternativeRecommendationModel(BaseModel):
    destination_id: str
    name: str
    similarity_score: float
    distance_km: float
    crowd_category: str
    reason: str

class TimeSlotSuggestionModel(BaseModel):
    date: str
    crowd_category: str

class RecommendationResponse(BaseModel):
    original_destination: Dict[str, Any]
    is_overcrowded: bool
    alternatives: List[AlternativeRecommendationModel]
    alternate_time_slots: List[TimeSlotSuggestionModel]

@recommend_router.get("/recommend/{destination_id}", response_model=RecommendationResponse)
def get_recommendations(destination_id: str, force_alternatives: bool = Query(False, description="Force recommendations even if not overcrowded")):
    try:
        # Validate that the destination exists in our metadata
        get_metadata_or_raise(destination_id)
        
        result = recommender.recommend(destination_id, force_alternatives=force_alternatives)
        
        # Convert internal dataclasses to Pydantic models for serialization
        alternatives = [
            AlternativeRecommendationModel(
                destination_id=alt.destination_id,
                name=alt.name,
                similarity_score=alt.similarity_score,
                distance_km=alt.distance_km,
                crowd_category=alt.crowd_category,
                reason=alt.reason
            ) for alt in result.alternatives
        ]
        
        alternate_time_slots = [
            TimeSlotSuggestionModel(
                date=slot.date,
                crowd_category=slot.crowd_category
            ) for slot in result.alternate_time_slots
        ]
        
        return RecommendationResponse(
            original_destination=result.original_destination,
            is_overcrowded=result.is_overcrowded,
            alternatives=alternatives,
            alternate_time_slots=alternate_time_slots
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {e}")
