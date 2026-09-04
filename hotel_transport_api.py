from fastapi import APIRouter, HTTPException
from hotel_data import HOTELS_DB
from hotel_model import predict_occupancy
from transport_data import get_hubs
from transport_router import suggest_route

ht_router = APIRouter(prefix="/hotel-transport", tags=["Hotels & Transport"])

@ht_router.get("/hotels/{destination_id}")
def api_get_hotels(destination_id: str):
    hotels = HOTELS_DB.get(destination_id, [])
    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found")
        
    result = []
    for h in hotels:
        # Get just today's forecast for the summary
        forecast = predict_occupancy(h["hotel_id"], days=1)
        occ = forecast[0]["occupancy_pct"] if forecast else 0
        cat = forecast[0]["demand_category"] if forecast else "Unknown"
        sug = forecast[0]["pricing_suggestion"] if forecast else ""
        
        result.append({
            **h,
            "current_occupancy": occ,
            "demand_category": cat,
            "pricing_suggestion": sug
        })
    return result

@ht_router.get("/hotel-forecast/{hotel_id}")
def api_get_hotel_forecast(hotel_id: str):
    forecast = predict_occupancy(hotel_id, days=7)
    if not forecast:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return forecast

@ht_router.get("/hubs/{destination_id}")
def api_get_hubs(destination_id: str):
    hubs = get_hubs(destination_id)
    return hubs

@ht_router.get("/route-suggestion/{destination_id}")
def api_get_route(destination_id: str):
    res = suggest_route(destination_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res
