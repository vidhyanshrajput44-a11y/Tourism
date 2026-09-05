import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class LocalBusiness:
    business_id: str
    destination_id: str
    name: str
    category: str # artisan, guide, food, experience
    description: str
    latitude: float
    longitude: float
    rating: float
    price_range: str # ₹, ₹₹, ₹₹₹
    contact_info: str
    opening_time: str
    closing_time: str

DESTINATIONS = [
    "taj_mahal", "jaipur_city_palace", "goa_baga_beach", "kerala_backwaters",
    "varanasi_ghats", "hampi_ruins", "manali", "mysore_palace",
    "agra_fort", "mehtab_bagh", "fatehpur_sikri", "nahargarh_fort", 
    "albert_hall_museum", "amer_fort", "anjuna_beach", "chapora_fort", 
    "morjim_beach", "marari_beach", "kumarakom_bird_sanctuary", "sarnath", 
    "ramnagar_fort", "matanga_hill", "sanapur_lake", "solang_valley", 
    "naggar_castle", "chamundi_hill", "brindavan_gardens"
]

CATEGORIES = ["artisan", "guide", "food", "experience"]
ADJECTIVES = ["Authentic", "Traditional", "Famous", "Local", "Heritage", "Royal"]
NOUNS = ["Crafts", "Tours", "Eats", "Adventures", "Bites", "Walks", "Textiles"]

def generate_businesses() -> List[LocalBusiness]:
    businesses = []
    # Seed fixed random for stable demo data
    rng = random.Random(42)
    
    for dest_id in DESTINATIONS:
        num_businesses = rng.randint(4, 6)
        for i in range(num_businesses):
            cat = rng.choice(CATEGORIES)
            adj = rng.choice(ADJECTIVES)
            noun = rng.choice(NOUNS)
            b_name = f"{adj} {dest_id.replace('_', ' ').title()} {noun}"
            
            businesses.append(LocalBusiness(
                business_id=f"biz_{dest_id}_{i}",
                destination_id=dest_id,
                name=b_name,
                category=cat,
                description=f"A highly rated {cat} offering unique local experiences near {dest_id.replace('_', ' ').title()}.",
                latitude=rng.uniform(10.0, 30.0), # Dummy coords
                longitude=rng.uniform(70.0, 90.0),
                rating=round(rng.uniform(3.8, 5.0), 1),
                price_range=rng.choice(["₹", "₹₹", "₹₹₹"]),
                contact_info=f"+91-999000{rng.randint(1000, 9999)}",
                opening_time="09:00 AM",
                closing_time="08:00 PM"
            ))
    return businesses

BUSINESSES = generate_businesses()

def get_businesses(destination_id: str) -> List[LocalBusiness]:
    return [b for b in BUSINESSES if b.destination_id == destination_id]
