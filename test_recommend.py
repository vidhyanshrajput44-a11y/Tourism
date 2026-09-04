import httpx
import time

def test_recommendations():
    base_url = "http://127.0.0.1:8000"
    
    print("Fetching list of destinations to find overcrowded ones...")
    try:
        response = httpx.get(f"{base_url}/destinations", timeout=10.0)
        response.raise_for_status()
        destinations = response.json()
    except Exception as e:
        print(f"Error connecting to server. Is it running on {base_url}? Error: {e}")
        return

    high_crowd_dests = [d for d in destinations if d.get("current_crowd_category") == "High"]
    
    if not high_crowd_dests:
        print("No currently overcrowded destinations found. Testing with a random destination instead...")
        test_dests = destinations[:2]
        force = True
    else:
        print(f"Found {len(high_crowd_dests)} overcrowded destinations. Testing up to 3...")
        test_dests = high_crowd_dests[:3]
        force = False

    for dest in test_dests:
        dest_id = dest["destination_id"]
        name = dest["name"]
        print(f"\n{'='*50}")
        print(f"Testing Recommendations for: {name} ({dest_id})")
        print(f"{'='*50}")
        
        try:
            rec_response = httpx.get(
                f"{base_url}/ui2/recommend/{dest_id}", 
                params={"force_alternatives": force},
                timeout=10.0
            )
            rec_response.raise_for_status()
            result = rec_response.json()
            
            orig = result["original_destination"]
            print(f"Original: {orig['name']} - Crowd: {orig['crowd_category']} (Score: {orig['crowd_score']})")
            
            alts = result["alternatives"]
            print(f"\nFound {len(alts)} Alternatives:")
            for i, alt in enumerate(alts, 1):
                print(f"  {i}. {alt['name']} ({alt['destination_id']})")
                print(f"     Distance: {alt['distance_km']}km | Similarity: {alt['similarity_score']:.2f} | Crowd: {alt['crowd_category']}")
                print(f"     Reason: {alt['reason']}")
            
            slots = result["alternate_time_slots"]
            if slots:
                print(f"\nFound {len(slots)} Alternate Time Slots (Low Crowd Days):")
                for slot in slots[:3]:
                    print(f"  - {slot['date']}: {slot['crowd_category']}")
            else:
                print("\nNo low-crowd days found in the next 7 days.")
                
        except Exception as e:
            print(f"Failed to get recommendations for {dest_id}: {e}")

if __name__ == "__main__":
    test_recommendations()
