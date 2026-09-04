import httpx

API_URL = "http://127.0.0.1:8000"

def run_test():
    print("=== TESTING UI 5: GOV DASHBOARD ===")
    
    # 1. Heatmap Data
    try:
        resp = httpx.get(f"{API_URL}/gov/heatmap-data")
        resp.raise_for_status()
        data = resp.json()
        print(f"\n[Heatmap Data] Fetched {len(data)} destinations")
        for d in data[:3]:
            print(f"- {d['name']}: {d['lat']}, {d['lon']} (Score: {d['crowd_score']})")
    except Exception as e:
        print("Error getting heatmap data:", e)

    # 2. What-If Simulation
    try:
        payload = {"destination_id": "taj_mahal", "proposed_cap": 5000} # Deliberately low to force overflow
        resp = httpx.post(f"{API_URL}/gov/whatif", json=payload)
        resp.raise_for_status()
        sim = resp.json()
        print(f"\n[What-If Simulation for Taj Mahal (Cap: 5000)]")
        print(f"Predicted Visitors: {sim['predicted_visitors']}")
        print(f"Simulated Score: {sim['simulated_crowd_score']} ({sim['simulated_crowd_category']})")
        print(f"Overflow: {sim['overflow_count']}")
        print(f"Recommendation: {sim['recommendation']}")
        if sim.get("redirect_suggestion"):
            print(f"Suggested Redirect: {sim['redirect_suggestion']['name']}")
    except Exception as e:
        print("Error running what-if:", e)

    # 3. Crowd Vision Estimation
    try:
        samples_resp = httpx.get(f"{API_URL}/gov/crowd-vision/samples")
        samples_resp.raise_for_status()
        samples = samples_resp.json()
        print(f"\n[CV Samples] Found: {samples}")
        
        for sample in samples:
            print(f"Running inference on {sample}...")
            # Form data
            data = {"destination_id": "taj_mahal", "sample_image_name": sample}
            resp = httpx.post(f"{API_URL}/gov/crowd-vision/estimate", data=data, timeout=30.0)
            resp.raise_for_status()
            cv = resp.json()
            print(f"- Detected: {cv['detected_count']} persons. Density Score: {cv['estimated_density_score']}")
    except Exception as e:
        print("Error running crowd vision:", e)

if __name__ == "__main__":
    run_test()
