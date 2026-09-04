import httpx

def run_tests():
    print("--- Testing UI 6: Hotel & Transport API ---\n")
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. Test Hotel Demand
    print("[1] Fetching hotels for Taj Mahal...")
    r = httpx.get(f"{base_url}/hotel-transport/hotels/taj_mahal")
    hotels = r.json()
    for h in hotels:
        print(f" - {h['name']} ({h['star_rating']} Star): {h['current_occupancy']}% Occupancy -> {h['demand_category']} Demand")
        print(f"   Suggestion: {h['pricing_suggestion']}")
    print()
    
    # 2. Test Hotel Forecast
    if hotels:
        hotel_id = hotels[0]["hotel_id"]
        print(f"[2] Fetching 7-day forecast for {hotels[0]['name']}...")
        r = httpx.get(f"{base_url}/hotel-transport/hotel-forecast/{hotel_id}")
        forecast = r.json()
        for f in forecast[:3]:
            print(f" - {f['date']}: {f['occupancy_pct']}% ({f['demand_category']})")
        print("   ... (truncated)\n")
        
    # 3. Test Transport Routing (Varanasi Ghats usually has high crowd score in UI 1 generator if it's weekend, but let's test a couple)
    for dest in ["taj_mahal", "varanasi_ghats"]:
        print(f"[3] Routing recommendation for {dest}:")
        r = httpx.get(f"{base_url}/hotel-transport/route-suggestion/{dest}")
        rec = r.json()
        print(" Hubs:")
        for h in rec.get("hubs", []):
            print(f"   - {h['name']}: {h['congestion_score']}/100 ({h['congestion_category']})")
        sug = rec.get("suggestion", {})
        print(f" Suggestion: {sug.get('message')} -> {sug.get('action')}\n")

if __name__ == "__main__":
    run_tests()
