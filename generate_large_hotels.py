import json
import random

destinations = [
    ("taj_mahal", "Agra", "CTCAGR"),
    ("jaipur_city_palace", "Jaipur", "CTCJAI"),
    ("goa_baga_beach", "Goa", "CTCGOA"),
    ("kerala_backwaters", "Alleppey", "CTCALP"),
    ("varanasi_ghats", "Varanasi", "CTCVNS"),
    ("hampi_ruins", "Hampi", "CTCHPI"),
    ("manali", "Manali", "CTCMAN"),
    ("mysore_palace", "Mysore", "CTCMYS")
]

prefixes = ["Taj", "Oberoi", "Radisson", "Hyatt", "Marriott", "ITC", "Lemon Tree", "Oyo", "Zostel", "FabHotel", "Royal", "Grand", "Heritage", "Boutique", "Golden", "Sunset", "Paradise", "Comfort", "Luxury", "Budget", "Holiday", "Resort", "Palace", "Inn", "Suites"]
suffixes = ["Hotel", "Resort", "Palace", "Inn", "Suites", "Retreat", "Lodge", "Villa", "Bhavan", "View"]

HOTELS_DB = {}

# We need 20 hotels per destination
for dest_id, city, mmt_code in destinations:
    hotels = []
    for i in range(1, 21):
        name = f"{random.choice(prefixes)} {random.choice(suffixes)} {city}"
        star = random.choice([3.0, 3.5, 4.0, 4.5, 5.0])
        rooms = random.randint(20, 250)
        
        if star >= 4.5:
            base_price = random.randint(10000, 35000)
        elif star >= 4.0:
            base_price = random.randint(5000, 12000)
        else:
            base_price = random.randint(800, 4000)
            
        img_id = random.randint(100, 999)
        image_url = f"https://picsum.photos/seed/hotel{dest_id}{i}/300/200"
        
        mmt_link = f"https://www.makemytrip.com/hotels/hotel-listing/?city={mmt_code}&searchText={name.replace(' ', '%20')}"
        
        hotels.append({
            "hotel_id": f"h_{dest_id[:3]}_{i}",
            "name": name,
            "star_rating": star,
            "total_rooms": rooms,
            "base_price": base_price,
            "image_url": image_url,
            "mmt_link": mmt_link
        })
    HOTELS_DB[dest_id] = hotels

with open("hotels_db_dump.json", "w") as f:
    json.dump(HOTELS_DB, f, indent=4)
print("Dumped!")
