import httpx
from transport_data import get_hubs
import random

def suggest_route(destination_id: str):
    hubs = get_hubs(destination_id)
    if not hubs:
        return {"error": "No transit hubs found for this destination"}
        
    try:
        resp = httpx.get("http://127.0.0.1:8000/destinations", timeout=5.0)
        resp.raise_for_status()
        dests = resp.json()
    except Exception as e:
        return {"error": str(e)}
        
    d_meta = next((d for d in dests if d["destination_id"] == destination_id), None)
    if not d_meta:
        return {"error": "Destination not found"}
        
    dest_crowd = d_meta["current_crowd_score"]
    
    # Simple heuristic: Transit hubs share the destination's congestion, 
    # but the primary hub (usually index 0) gets the brunt of it.
    
    hub_status = []
    for i, h in enumerate(hubs):
        # Primary hub takes full congestion. Alternate hubs take 60% congestion.
        mult = 1.0 if i == 0 else random.uniform(0.5, 0.7)
        score = int(dest_crowd * mult)
        cat = "Low" if score < 40 else "Medium" if score < 70 else "High"
        hub_status.append({
            "hub_id": h["hub_id"],
            "name": h["name"],
            "type": h["type"],
            "congestion_score": score,
            "congestion_category": cat
        })
        
    primary = hub_status[0]
    
    # Routing recommendation logic
    recommendation = {
        "destination_id": destination_id,
        "hubs": hub_status,
        "suggestion": None
    }
    
    if primary["congestion_category"] == "High" or primary["congestion_score"] > 65:
        # Find the best alternative
        alternatives = sorted([h for h in hub_status if h["hub_id"] != primary["hub_id"]], key=lambda x: x["congestion_score"])
        if alternatives:
            alt = alternatives[0]
            recommendation["suggestion"] = {
                "message": f"Primary hub ({primary['name']}) is highly congested.",
                "action": f"Consider using {alt['name']} ({alt['type'].replace('_', ' ')}) instead, which has {alt['congestion_category'].lower()} congestion."
            }
        else:
            recommendation["suggestion"] = {
                "message": f"Primary hub ({primary['name']}) is congested, but no viable alternatives exist.",
                "action": "Expect delays."
            }
    else:
        recommendation["suggestion"] = {
            "message": f"Primary hub ({primary['name']}) has manageable congestion.",
            "action": "Proceed with default transit route."
        }
        
    return recommendation
