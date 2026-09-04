import httpx

API_URL = "http://127.0.0.1:8000"

def run_test():
    print("=== TESTING UI 4: LOCAL MARKET & HIDDEN GEMS ===")
    
    # Test Hidden Gems
    try:
        resp = httpx.get(f"{API_URL}/local/hidden-gems")
        resp.raise_for_status()
        gems = resp.json()
        print("\n[Hidden Gems Top 5]")
        for g in gems[:5]:
            print(f"- {g['name']} (Score: {g['hidden_gem_score']}, Rating: {g['quality_rating']}, Crowd: {g['crowd_category']})")
    except Exception as e:
        print("Error getting hidden gems:", e)

    # Test Local Businesses for Taj Mahal
    try:
        resp = httpx.get(f"{API_URL}/local/businesses/taj_mahal")
        resp.raise_for_status()
        biz = resp.json()
        print(f"\n[Local Businesses - Taj Mahal] Found {len(biz)}")
        for b in biz[:3]:
            print(f"- {b['name']} ({b['category']}, {b['rating']} stars)")
    except Exception as e:
        print("Error getting businesses:", e)

    # Test Businesses Near Alternative
    try:
        resp = httpx.get(f"{API_URL}/local/businesses-near-alternative/taj_mahal")
        resp.raise_for_status()
        biz_alt = resp.json()
        print(f"\n[Businesses Near Alternative for Taj Mahal] Found {len(biz_alt)}")
        for b in biz_alt[:3]:
            print(f"- {b['name']} ({b['category']}, {b['rating']} stars) - Dest ID: {b['destination_id']}")
    except Exception as e:
        print("Error getting businesses near alternative:", e)

if __name__ == "__main__":
    run_test()
