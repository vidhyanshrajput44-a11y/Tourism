import httpx
import json
import time

destinations = [
    "agra_fort", "mehtab_bagh", "fatehpur_sikri",
    "nahargarh_fort", "albert_hall_museum", "amer_fort",
    "anjuna_beach", "chapora_fort", "morjim_beach",
    "marari_beach", "kumarakom_bird_sanctuary",
    "sarnath", "ramnagar_fort",
    "matanga_hill", "sanapur_lake",
    "solang_valley", "naggar_castle",
    "chamundi_hill", "brindavan_gardens"
]

queries = {
    "agra_fort": "agra fort india",
    "mehtab_bagh": "mehtab bagh agra",
    "fatehpur_sikri": "fatehpur sikri",
    "nahargarh_fort": "nahargarh fort",
    "albert_hall_museum": "albert hall museum",
    "amer_fort": "amer fort jaipur",
    "anjuna_beach": "anjuna beach goa",
    "chapora_fort": "chapora fort",
    "morjim_beach": "morjim beach",
    "marari_beach": "marari beach kerala",
    "kumarakom_bird_sanctuary": "kumarakom kerala",
    "sarnath": "sarnath",
    "ramnagar_fort": "ramnagar fort varanasi",
    "matanga_hill": "matanga hill hampi",
    "sanapur_lake": "hampi lake",
    "solang_valley": "solang valley",
    "naggar_castle": "naggar castle",
    "chamundi_hill": "chamundi hill",
    "brindavan_gardens": "brindavan gardens"
}

results = {}
headers = {'User-Agent': 'Mozilla/5.0'}

for dest_id, query in queries.items():
    url = f"https://unsplash.com/napi/search/photos?query={query.replace(' ', '+')}&per_page=1"
    try:
        with httpx.Client(verify=False) as client:
            resp = client.get(url, headers=headers)
            data = resp.json()
            if data['results']:
                photo = data['results'][0]
                results[dest_id] = {
                    "photo": photo['id'],
                    "alt": photo.get('alt_description', query),
                    "credit": photo['user']['name'],
                    "creditUrl": photo['user']['links']['html'],
                    "photoUrl": photo['links']['html']
                }
            else:
                print(f"No results for {dest_id}")
    except Exception as e:
        print(f"Error for {dest_id}: {e}")
    time.sleep(0.5)

print(json.dumps(results, indent=2))
