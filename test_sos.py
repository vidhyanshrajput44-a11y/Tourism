import httpx

API_URL = "http://127.0.0.1:8000"

def run_test():
    print("=== TESTING UI 3: SMART SAFETY & SOS ===")
    
    # 1. Check if the help-points API works
    try:
        resp = httpx.get(f"{API_URL}/safety/help-points/taj_mahal")
        resp.raise_for_status()
        print(f"\n[GET /safety/help-points/taj_mahal] Found {len(resp.json())} help points.")
    except Exception as e:
        print("Failed to get help points:", e)
        return

    # 2. Simulate SOS from a tourist visiting Taj Mahal (near the destination)
    print("\n--- Triggering SOS ---")
    sos_payload = {
        "user_id": "user_demo_001",
        "lat": 27.1760,
        "lon": 78.0430,
        "emergency_contacts": ["+91-9876543210", "+91-1122334455"]
    }
    
    resp = httpx.post(f"{API_URL}/safety/sos", json=sos_payload)
    resp.raise_for_status()
    
    result = resp.json()
    print("SOS Trigger Result:")
    print(f"Status: {result.get('status')}")
    print(f"Alerts sent to: {result.get('alert_sent_to')}")
    print(f"ETA Message: {result.get('eta_message')}")
    
    hospital = result.get('nearest_hospital')
    police = result.get('nearest_police')
    if hospital:
        print(f"\nNearest Hospital: {hospital['name']} ({hospital['phone_number']})")
    if police:
        print(f"Nearest Police: {police['name']} ({police['phone_number']})")

if __name__ == "__main__":
    run_test()
