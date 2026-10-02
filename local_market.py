import httpx
from typing import List, Dict, Any, Optional
from local_market_data import get_businesses, LocalBusiness

def get_local_businesses(destination_id: str, category_filter: Optional[str] = None) -> List[LocalBusiness]:
    businesses = get_businesses(destination_id)
    if category_filter:
        businesses = [b for b in businesses if b.category.lower() == category_filter.lower()]
    return sorted(businesses, key=lambda x: x.rating, reverse=True)

def get_businesses_near_alternative(destination_id: str) -> List[LocalBusiness]:
    try:
        from recommender import CrowdRecommender
        rec = CrowdRecommender()
        res = rec.recommend(destination_id, force_alternatives=True)
        if res.alternatives:
            top_alt_id = res.alternatives[0].destination_id
            return get_local_businesses(top_alt_id)
    except Exception:
        pass

    try:
        resp = httpx.get(f"http://127.0.0.1:8000/ui2/recommend/{destination_id}?force_alternatives=true", timeout=5.0)
        data = resp.json()
        alts = data.get("alternatives", [])
        if not alts:
            return []
        top_alt_id = alts[0]["destination_id"]
        return get_local_businesses(top_alt_id)
    except Exception as e:
        print(f"Error calling UI 2 recommendations: {e}")
        return []
