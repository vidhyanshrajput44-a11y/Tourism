import httpx

API_URL = "http://127.0.0.1:8000"

def run_test():
    print("=== TESTING UI 3: SAFE ROUTING ===")
    
    # Let's get the risk zones for Taj Mahal to know where they are
    resp = httpx.get(f"{API_URL}/safety/risk-zones/taj_mahal")
    zones = resp.json()
    print(f"\n[Risk Zones for Taj Mahal]: {len(zones)} found")
    for z in zones:
        print(f" - {z['risk_level']} risk ({z['risk_type']}) at {z['latitude']}, {z['longitude']} (radius: {z['radius_meters']}m)")
    
    if len(zones) == 0:
        print("No zones to test.")
        return

    # A zone is at lat: 27.1801, lon: 78.0471 (approx). Let's trace a line through it.
    target_zone = zones[0]
    
    # Test 1: A route directly passing through the target zone
    print("\n--- Test 1: Unsafe Route (passes through zone) ---")
    unsafe_payload = {
        "destination_id": "taj_mahal",
        "start_lat": target_zone['latitude'] - 0.005,
        "start_lon": target_zone['longitude'] - 0.005,
        "end_lat": target_zone['latitude'] + 0.005,
        "end_lon": target_zone['longitude'] + 0.005
    }
    resp1 = httpx.post(f"{API_URL}/safety/safe-route", json=unsafe_payload)
    res1 = resp1.json()
    print(f"Is safe? {res1['is_safe']}")
    for w in res1['warnings']:
        print(f"WARNING: {w}")
    if res1['suggested_waypoints']:
        print("Suggested waypoint to bypass:", res1['suggested_waypoints'][0])

    # Test 2: A safe route far from the zone
    print("\n--- Test 2: Safe Route (far away) ---")
    safe_payload = {
        "destination_id": "taj_mahal",
        "start_lat": target_zone['latitude'] + 0.05,
        "start_lon": target_zone['longitude'] + 0.05,
        "end_lat": target_zone['latitude'] + 0.06,
        "end_lon": target_zone['longitude'] + 0.06
    }
    resp2 = httpx.post(f"{API_URL}/safety/safe-route", json=safe_payload)
    res2 = resp2.json()
    print(f"Is safe? {res2['is_safe']}")
    if res2['warnings']:
        for w in res2['warnings']:
            print(f"WARNING: {w}")
    else:
        print("No warnings! Route is clean.")


if __name__ == "__main__":
    run_test()
