import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

def build_knowledge_base():
    print("Building knowledge base from live endpoints...")
    documents = []
    
    with httpx.Client(timeout=10.0) as client:
        # 1. Destinations & Crowd Intelligence (UI 1)
        try:
            r = client.get(f"{BASE_URL}/destinations")
            if r.status_code == 200:
                dests = r.json()
                for d in dests:
                    did = d["destination_id"]
                    doc = f"{d['name']} is a destination in {d['city']}, {d['state']}. The current crowd index is {d['current_crowd_score']}/100 ({d['crowd_category']}). Max capacity is {d['max_capacity']} visitors/day."
                    documents.append({"text": doc, "source_module": "Crowd Intelligence", "destination_id": did})
                    
                    # Forecast
                    fr = client.get(f"{BASE_URL}/forecast/{did}")
                    if fr.status_code == 200:
                        forecast = fr.json()
                        f_docs = [f"On {f['date']}, {d['name']} is expected to have a crowd index of {f['crowd_score']}/100 ({f['crowd_category']})." for f in forecast]
                        for fd in f_docs:
                            documents.append({"text": fd, "source_module": "Crowd Intelligence", "destination_id": did})
        except Exception as e:
            print("Error fetching UI 1 data:", e)

        # 2. Recommendations (UI 2)
        try:
            if 'dests' in locals():
                for d in dests:
                    did = d["destination_id"]
                    rr = client.get(f"{BASE_URL}/recommend/{did}")
                    if rr.status_code == 200:
                        rec = rr.json()
                        for alt in rec.get("recommended_alternatives", []):
                            doc = f"A less crowded alternative to {d['name']} is {alt['name']} in {alt['city']}, {alt['state']}. It currently has a crowd score of {alt['current_crowd_score']}/100."
                            documents.append({"text": doc, "source_module": "Recommendation Engine", "destination_id": did})
        except Exception as e:
            print("Error fetching UI 2 data:", e)

        # 3. Safety (UI 3)
        try:
            if 'dests' in locals():
                for d in dests:
                    did = d["destination_id"]
                    sr = client.get(f"{BASE_URL}/safety/risk-zones/{did}")
                    if sr.status_code == 200:
                        for rz in sr.json():
                            doc = f"{d['name']} has a {rz['risk_level']} risk zone due to {rz['risk_type']}."
                            documents.append({"text": doc, "source_module": "Smart Safety", "destination_id": did})
                    
                    hr = client.get(f"{BASE_URL}/safety/help-points/{did}")
                    if hr.status_code == 200:
                        for hp in hr.json():
                            doc = f"At {d['name']}, there is a {hp['type']} help point named '{hp['name']}'. Contact: {hp.get('phone_number', 'N/A')}."
                            documents.append({"text": doc, "source_module": "Smart Safety", "destination_id": did})
        except Exception as e:
            print("Error fetching UI 3 data:", e)

        # 4. Local Market & Hidden Gems (UI 4)
        try:
            hgr = client.get(f"{BASE_URL}/local/hidden-gems")
            if hgr.status_code == 200:
                for hg in hgr.json():
                    doc = f"{hg['name']} is a highly rated hidden gem (Gem Score: {hg['hidden_gem_score']}). Reason: {hg['reason']}."
                    documents.append({"text": doc, "source_module": "Hidden Gems", "destination_id": hg["destination_id"]})
                    
            if 'dests' in locals():
                for d in dests:
                    did = d["destination_id"]
                    br = client.get(f"{BASE_URL}/local/businesses/{did}")
                    if br.status_code == 200:
                        for b in br.json()[:5]: # Take top 5 to save space
                            doc = f"Local business near {d['name']}: {b['name']} is a {b['category']} ({b['price_range']}). Rating: {b['rating']} stars. {b['description']}. Contact: {b['contact_info']}."
                            documents.append({"text": doc, "source_module": "Local Market Connect", "destination_id": did})
        except Exception as e:
            print("Error fetching UI 4 data:", e)

        # 6. Hotels & Transport (UI 6)
        try:
            if 'dests' in locals():
                for d in dests:
                    did = d["destination_id"]
                    # Hotels
                    htr = client.get(f"{BASE_URL}/hotel-transport/hotels/{did}")
                    if htr.status_code == 200:
                        for h in htr.json():
                            doc = f"Hotel near {d['name']}: {h['name']} ({h['star_rating']} stars) has {h['total_rooms']} rooms. Today's occupancy is {h['current_occupancy']}%. Demand is {h['demand_category']}. Suggestion: {h['pricing_suggestion']}."
                            documents.append({"text": doc, "source_module": "Hotel Demand Engine", "destination_id": did})
                    
                    # Transport
                    tr = client.get(f"{BASE_URL}/hotel-transport/route-suggestion/{did}")
                    if tr.status_code == 200:
                        tr_data = tr.json()
                        sug = tr_data.get("suggestion", {})
                        doc = f"Transport routing for {d['name']}: {sug.get('message')}. Action: {sug.get('action')}."
                        documents.append({"text": doc, "source_module": "Crowd-Aware Transport", "destination_id": did})
                        for hub in tr_data.get("hubs", []):
                            doc = f"Transit hub for {d['name']}: {hub['name']} ({hub['type']}) has a congestion score of {hub['congestion_score']}/100 ({hub['congestion_category']})."
                            documents.append({"text": doc, "source_module": "Crowd-Aware Transport", "destination_id": did})
        except Exception as e:
            print("Error fetching UI 6 data:", e)

    print(f"Built knowledge base with {len(documents)} documents.")
    with open("knowledge_base.json", "w") as f:
        json.dump(documents, f)
    return documents

if __name__ == "__main__":
    build_knowledge_base()
