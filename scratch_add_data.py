import json
from pathlib import Path

metadata_path = Path("/Users/vidhyanshrajput/Desktop/tourism app/data/destination_metadata.json")

with open(metadata_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_locations = [
    # Agra (Alternatives to Taj Mahal)
    {
        "destination_id": "agra_fort",
        "name": "Agra Fort",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "category": "heritage",
        "tags": ["fort", "mughal", "architecture", "unesco", "history"],
        "latitude": 27.1795,
        "longitude": 78.0211,
        "average_visit_duration_hours": 2.0,
        "ideal_for": ["family", "couple", "solo"]
    },
    {
        "destination_id": "mehtab_bagh",
        "name": "Mehtab Bagh",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "category": "heritage",
        "tags": ["garden", "taj view", "mughal", "photography", "scenic"],
        "latitude": 27.1795,
        "longitude": 78.0426,
        "average_visit_duration_hours": 1.5,
        "ideal_for": ["couple", "solo"]
    },
    {
        "destination_id": "fatehpur_sikri",
        "name": "Fatehpur Sikri",
        "city": "Agra",
        "state": "Uttar Pradesh",
        "category": "heritage",
        "tags": ["fort", "historical", "mughal", "unesco", "history"],
        "latitude": 27.0945,
        "longitude": 77.6679,
        "average_visit_duration_hours": 3.0,
        "ideal_for": ["family", "solo"]
    },
    # Jaipur (Alternatives to City Palace)
    {
        "destination_id": "nahargarh_fort",
        "name": "Nahargarh Fort",
        "city": "Jaipur",
        "state": "Rajasthan",
        "category": "heritage",
        "tags": ["fort", "viewpoint", "sunset", "architecture", "history"],
        "latitude": 26.9372,
        "longitude": 75.8155,
        "average_visit_duration_hours": 2.5,
        "ideal_for": ["couple", "adventure"]
    },
    {
        "destination_id": "albert_hall_museum",
        "name": "Albert Hall Museum",
        "city": "Jaipur",
        "state": "Rajasthan",
        "category": "heritage",
        "tags": ["museum", "art", "history", "architecture", "indo-saracenic"],
        "latitude": 26.9116,
        "longitude": 75.8195,
        "average_visit_duration_hours": 2.0,
        "ideal_for": ["family", "solo"]
    },
    {
        "destination_id": "amer_fort",
        "name": "Amer Fort",
        "city": "Jaipur",
        "state": "Rajasthan",
        "category": "heritage",
        "tags": ["fort", "palace", "rajasthan", "architecture", "unesco"],
        "latitude": 26.9855,
        "longitude": 75.8513,
        "average_visit_duration_hours": 3.5,
        "ideal_for": ["family", "couple", "solo"]
    },
    # Goa (Alternatives to Baga Beach)
    {
        "destination_id": "anjuna_beach",
        "name": "Anjuna Beach",
        "city": "North Goa",
        "state": "Goa",
        "category": "beach",
        "tags": ["beach", "party", "flea market", "sunset", "coastal"],
        "latitude": 15.5793,
        "longitude": 73.7384,
        "average_visit_duration_hours": 4.0,
        "ideal_for": ["solo", "adventure", "couple"]
    },
    {
        "destination_id": "chapora_fort",
        "name": "Chapora Fort",
        "city": "North Goa",
        "state": "Goa",
        "category": "heritage",
        "tags": ["fort", "viewpoint", "sunset", "history", "ruins"],
        "latitude": 15.6030,
        "longitude": 73.7346,
        "average_visit_duration_hours": 1.5,
        "ideal_for": ["couple", "adventure"]
    },
    {
        "destination_id": "morjim_beach",
        "name": "Morjim Beach",
        "city": "North Goa",
        "state": "Goa",
        "category": "beach",
        "tags": ["beach", "serene", "turtles", "peaceful", "nature"],
        "latitude": 15.6178,
        "longitude": 73.7360,
        "average_visit_duration_hours": 3.0,
        "ideal_for": ["family", "couple"]
    },
    # Kerala (Alternatives to Alleppey)
    {
        "destination_id": "marari_beach",
        "name": "Marari Beach",
        "city": "Alleppey",
        "state": "Kerala",
        "category": "beach",
        "tags": ["beach", "relaxation", "serene", "nature", "coastal"],
        "latitude": 9.5960,
        "longitude": 76.2985,
        "average_visit_duration_hours": 3.0,
        "ideal_for": ["couple", "family"]
    },
    {
        "destination_id": "kumarakom_bird_sanctuary",
        "name": "Kumarakom Bird Sanctuary",
        "city": "Kumarakom",
        "state": "Kerala",
        "category": "wildlife",
        "tags": ["birds", "nature", "wildlife", "lake", "photography"],
        "latitude": 9.6264,
        "longitude": 76.4258,
        "average_visit_duration_hours": 2.0,
        "ideal_for": ["family", "solo", "adventure"]
    },
    # Varanasi (Alternatives to Ghats)
    {
        "destination_id": "sarnath",
        "name": "Sarnath",
        "city": "Varanasi",
        "state": "Uttar Pradesh",
        "category": "religious",
        "tags": ["buddhism", "stupa", "history", "peaceful", "heritage"],
        "latitude": 25.3811,
        "longitude": 83.0214,
        "average_visit_duration_hours": 2.5,
        "ideal_for": ["solo", "family"]
    },
    {
        "destination_id": "ramnagar_fort",
        "name": "Ramnagar Fort",
        "city": "Varanasi",
        "state": "Uttar Pradesh",
        "category": "heritage",
        "tags": ["fort", "museum", "history", "architecture", "river view"],
        "latitude": 25.2698,
        "longitude": 83.0267,
        "average_visit_duration_hours": 2.0,
        "ideal_for": ["family", "solo"]
    },
    # Hampi
    {
        "destination_id": "matanga_hill",
        "name": "Matanga Hill",
        "city": "Hampi",
        "state": "Karnataka",
        "category": "hill-station",
        "tags": ["trekking", "viewpoint", "sunrise", "nature", "adventure"],
        "latitude": 15.3340,
        "longitude": 76.4627,
        "average_visit_duration_hours": 2.0,
        "ideal_for": ["adventure", "solo"]
    },
    {
        "destination_id": "sanapur_lake",
        "name": "Sanapur Lake",
        "city": "Hampi",
        "state": "Karnataka",
        "category": "wildlife",
        "tags": ["lake", "nature", "coracle ride", "scenic", "relaxation"],
        "latitude": 15.3620,
        "longitude": 76.4411,
        "average_visit_duration_hours": 2.5,
        "ideal_for": ["couple", "adventure"]
    },
    # Manali
    {
        "destination_id": "solang_valley",
        "name": "Solang Valley",
        "city": "Manali",
        "state": "Himachal Pradesh",
        "category": "hill-station",
        "tags": ["adventure", "snow", "mountains", "scenic", "sports"],
        "latitude": 32.3168,
        "longitude": 77.1558,
        "average_visit_duration_hours": 4.0,
        "ideal_for": ["adventure", "family", "couple"]
    },
    {
        "destination_id": "naggar_castle",
        "name": "Naggar Castle",
        "city": "Manali",
        "state": "Himachal Pradesh",
        "category": "heritage",
        "tags": ["castle", "architecture", "history", "art", "scenic"],
        "latitude": 32.1154,
        "longitude": 77.1728,
        "average_visit_duration_hours": 2.0,
        "ideal_for": ["couple", "solo"]
    },
    # Mysore
    {
        "destination_id": "chamundi_hill",
        "name": "Chamundi Hill",
        "city": "Mysuru",
        "state": "Karnataka",
        "category": "religious",
        "tags": ["temple", "viewpoint", "hill", "spiritual", "nature"],
        "latitude": 12.2741,
        "longitude": 76.6713,
        "average_visit_duration_hours": 2.5,
        "ideal_for": ["family", "solo"]
    },
    {
        "destination_id": "brindavan_gardens",
        "name": "Brindavan Gardens",
        "city": "Mysuru",
        "state": "Karnataka",
        "category": "wildlife",
        "tags": ["garden", "fountains", "lights", "nature", "family"],
        "latitude": 12.4244,
        "longitude": 76.5724,
        "average_visit_duration_hours": 3.0,
        "ideal_for": ["family", "couple"]
    }
]

# Ensure we don't duplicate
existing_ids = {d["destination_id"] for d in data}
for loc in new_locations:
    if loc["destination_id"] not in existing_ids:
        data.append(loc)

with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Added {len(new_locations)} alternative locations to destination_metadata.json")
