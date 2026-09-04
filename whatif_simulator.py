import httpx
from datetime import datetime
from gov_dashboard_data import add_policy_log

def simulate_capacity_cap(destination_id: str, proposed_cap: int):
    # Fetch live forecast
    try:
        resp = httpx.get(f"http://127.0.0.1:8000/forecast/{destination_id}", timeout=5.0)
        resp.raise_for_status()
        forecast = resp.json()
    except Exception as e:
        print(f"Error fetching forecast for simulation: {e}")
        return {"error": "Could not fetch current forecast"}

    # Use today's predicted score (first item)
    today = forecast[0]
    crowd_score = today["crowd_score"]
    
    # We need to know original max capacity. Fetch destinations.
    try:
        dest_resp = httpx.get("http://127.0.0.1:8000/destinations", timeout=5.0)
        dests = dest_resp.json()
        d_meta = next((d for d in dests if d["destination_id"] == destination_id), None)
        if not d_meta:
            return {"error": "Destination not found"}
        original_cap = d_meta["max_capacity"]
    except Exception as e:
        return {"error": str(e)}

    # Estimate raw headcount from the score
    predicted_visitors = int((crowd_score / 100.0) * original_cap)
    
    # Simulate new score against proposed cap
    if proposed_cap <= 0:
        simulated_score = 100
    else:
        simulated_score = int((predicted_visitors / proposed_cap) * 100)
    simulated_score = min(100, simulated_score)
    
    sim_cat = "Low" if simulated_score < 40 else "Medium" if simulated_score < 70 else "High"
    
    overflow_count = max(0, predicted_visitors - proposed_cap)
    
    result = {
        "destination_id": destination_id,
        "name": d_meta["name"],
        "proposed_cap": proposed_cap,
        "predicted_visitors": predicted_visitors,
        "original_crowd_score": crowd_score,
        "original_crowd_category": today["crowd_category"],
        "simulated_crowd_score": simulated_score,
        "simulated_crowd_category": sim_cat,
        "overflow_count": overflow_count,
        "recommendation": "",
        "redirect_suggestion": None
    }
    
    if overflow_count > 0:
        result["recommendation"] = f"Warning: {overflow_count} visitors exceed the proposed cap. Consider redirecting overflow."
        try:
            rec_resp = httpx.get(f"http://127.0.0.1:8000/recommend/{destination_id}", timeout=5.0)
            rec_data = rec_resp.json()
            alts = rec_data.get("alternatives", [])
            if alts:
                result["redirect_suggestion"] = alts[0]
        except Exception:
            pass
    else:
        result["recommendation"] = "Cap is workable. Current predicted visitors fall within limits."

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "destination_id": destination_id,
        "proposed_cap": proposed_cap,
        "overflow_count": overflow_count,
        "simulated_category": sim_cat
    }
    add_policy_log(log_entry)
    
    return result
