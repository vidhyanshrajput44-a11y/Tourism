import httpx

# We just need lat/lon mapping for the 8 main destinations
DESTINATION_COORDS = {
    "taj_mahal": {"lat": 27.1751, "lon": 78.0421},
    "jaipur_city_palace": {"lat": 26.9255, "lon": 75.8236},
    "goa_baga_beach": {"lat": 15.5523, "lon": 73.7516},
    "kerala_backwaters": {"lat": 9.5009, "lon": 76.3364},
    "varanasi_ghats": {"lat": 25.2820, "lon": 83.0065},
    "hampi_ruins": {"lat": 15.3350, "lon": 76.4600},
    "manali": {"lat": 32.2396, "lon": 77.1887},
    "mysore_palace": {"lat": 12.3052, "lon": 76.6552},
}

# In-memory log of policy simulations run
POLICY_LOG = []

def get_heatmap_data():
    try:
        resp = httpx.get("http://127.0.0.1:8000/destinations", timeout=5.0)
        dests = resp.json()
    except Exception as e:
        print(f"Error fetching destinations for heatmap: {e}")
        return []

    import random
    
    heatmap_data = []
    for d in dests:
        coords = DESTINATION_COORDS.get(d["destination_id"])
        if coords:
            # Main Marker
            heatmap_data.append({
                "destination_id": d["destination_id"],
                "name": d["name"],
                "lat": coords["lat"],
                "lon": coords["lon"],
                "crowd_score": d["current_crowd_score"],
                "crowd_category": d["current_crowd_category"],
                "max_capacity": d["max_capacity"]
            })
            # Generate 3 scattered sub-markers for a localized heatmap effect
            for i in range(3):
                offset_lat = random.uniform(-0.015, 0.015)
                offset_lon = random.uniform(-0.015, 0.015)
                sub_score = max(0, min(100, d["current_crowd_score"] + random.randint(-15, 15)))
                sub_cat = "Low" if sub_score < 40 else "Medium" if sub_score < 70 else "High"
                
                heatmap_data.append({
                    "destination_id": f"{d['destination_id']}_sub_{i}",
                    "name": f"{d['name']} Zone {i+1}",
                    "lat": coords["lat"] + offset_lat,
                    "lon": coords["lon"] + offset_lon,
                    "crowd_score": sub_score,
                    "crowd_category": sub_cat,
                    "max_capacity": int(d["max_capacity"] * 0.2)
                })
    return heatmap_data

def add_policy_log(entry: dict):
    POLICY_LOG.insert(0, entry) # Add to front
    if len(POLICY_LOG) > 50:
        POLICY_LOG.pop()
