import json
import random

with open("data/destination_metadata.json", "r") as f:
    data = json.load(f)

# The 8 main destinations
main_dests = {d["destination_id"]: d for d in data[:8]}

attraction_types = [
    "Museum", "Art Gallery", "Botanical Garden", "Lake", "Temple", "Heritage Walk",
    "Local Market", "Bird Sanctuary", "Fort Ruins", "Viewpoint", "Palace", 
    "Cultural Center", "Handicraft Village", "Stepwell", "National Park", "Riverfront",
    "Memorial", "Observatory", "Spice Garden", "Aquarium"
]

categories = ["heritage", "beach", "hill-station", "wildlife", "religious"]
tags_pool = ["history", "photography", "nature", "peaceful", "crowded", "shopping", "architecture", "scenic", "sunset", "adventure"]
ideal_pool = ["family", "couple", "solo", "adventure"]

new_destinations = []

for main_id, main_data in main_dests.items():
    city = main_data["city"]
    state = main_data["state"]
    base_lat = main_data["latitude"]
    base_lon = main_data["longitude"]
    
    # Generate 15 alternatives
    for i in range(1, 16):
        attraction = random.choice(attraction_types)
        name = f"{city} {attraction} {i}"
        
        # slight coordinate shift (approx 1-30 km away)
        # 1 degree is ~111km. So 30km is ~0.27 degrees
        lat_shift = random.uniform(-0.15, 0.15)
        lon_shift = random.uniform(-0.15, 0.15)
        
        new_destinations.append({
            "destination_id": f"alt_{main_id}_{i}",
            "name": name,
            "city": city,
            "state": state,
            "category": random.choice(categories),
            "tags": random.sample(tags_pool, 3),
            "latitude": round(base_lat + lat_shift, 4),
            "longitude": round(base_lon + lon_shift, 4),
            "average_visit_duration_hours": round(random.uniform(1.0, 4.0), 1),
            "ideal_for": random.sample(ideal_pool, random.randint(1, 3))
        })

data.extend(new_destinations)

with open("data/destination_metadata.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Added {len(new_destinations)} new alternative destinations!")
