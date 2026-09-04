import httpx
from typing import List, Dict, Any
from hidden_gems_data import QUALITY_RATINGS

def get_hidden_gems(exclude_top: int = 3) -> List[Dict[str, Any]]:
    # Call UI 1 to get footfall/crowd data
    try:
        resp = httpx.get("http://127.0.0.1:8000/destinations", timeout=5.0)
        ui1_dests = resp.json()
    except Exception as e:
        print(f"Error calling UI 1 destinations: {e}")
        ui1_dests = []

    crowd_map = {d["destination_id"]: d["current_crowd_score"] for d in ui1_dests}

    gems = []
    for dest_id, rating in QUALITY_RATINGS.items():
        # If not tracked by UI 1 directly, assume it's an alternative with low crowd (25)
        crowd_score = crowd_map.get(dest_id, 25)
        
        # Calculate hidden gem score: quality_rating_normalized * 0.6 + (1 - crowd_index/100) * 0.4
        rating_norm = rating / 5.0
        crowd_norm = crowd_score / 100.0
        hidden_gem_score = (rating_norm * 0.6) + ((1.0 - crowd_norm) * 0.4)
        
        crowd_cat = "Low" if crowd_score < 40 else "Medium" if crowd_score < 70 else "High"
        
        reason = f"High-rated ({rating}/5), low-crowd alternative." if crowd_cat == "Low" else f"Rated {rating}/5, currently {crowd_cat} crowd."
        
        gems.append({
            "destination_id": dest_id,
            "name": dest_id.replace("_", " ").title(),
            "hidden_gem_score": round(hidden_gem_score, 3),
            "quality_rating": rating,
            "crowd_score": crowd_score,
            "crowd_category": crowd_cat,
            "reason": reason
        })

    # Sort all destinations by crowd_score descending to find the top most crowded/famous ones
    most_crowded = sorted(gems, key=lambda x: x["crowd_score"], reverse=True)
    exclude_ids = [g["destination_id"] for g in most_crowded[:exclude_top]]

    # Filter out the excluded ones and sort the rest by hidden_gem_score descending
    final_gems = [g for g in gems if g["destination_id"] not in exclude_ids]
    final_gems.sort(key=lambda x: x["hidden_gem_score"], reverse=True)
    
    return final_gems
