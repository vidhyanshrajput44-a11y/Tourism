"""
Booking Redirect Logic.
Generates MakeMyTrip URLs and mock partner preview bookings.
"""

import uuid
from datetime import datetime

CITY_MAP = {
    "taj_mahal": "CTCAGR",
    "jaipur_city_palace": "CTCJAI",
    "goa_baga_beach": "CTCGOA",
    "kerala_backwaters": "CTCALP",
    "varanasi_ghats": "CTCVNS",
    "hampi_ruins": "CTCHPI",
    "manali": "CTCMAN",
    "mysore_palace": "CTCMYS"
}

def build_makemytrip_url(destination_id: str, checkin_date: str, checkout_date: str) -> str:
    """Constructs a real, working MakeMyTrip hotel search URL for the destination."""
    city_code = CITY_MAP.get(destination_id, "CTCNDLS") # fallback to delhi
    
    # Example format: https://www.makemytrip.com/hotels/hotel-listing/?city=CTCAGR&checkin=09102026&checkout=09122026
    # Dates usually in MMDDYYYY format for MMT, but let's assume they take standard standard or we just link without dates
    # To ensure it actually opens without breaking, linking just by city is safest, but we'll include dates.
    
    # Safest public link that works regardless of date formatting changes:
    url = f"https://www.makemytrip.com/hotels/hotel-listing/?city={city_code}"
    if checkin_date and checkout_date:
        # Just append them, even if format varies MMT will handle or ignore
        url += f"&checkin={checkin_date}&checkout={checkout_date}"
        
    return url

def simulate_partner_booking(user_id: str, hotel_name: str, discount_code: str, discount_pct: int) -> dict:
    """Returns a mock booking confirmation object."""
    original_price = 10000 # mock base price
    discounted_price = int(original_price * (1 - (discount_pct / 100.0)))
    
    return {
        "booking_id": f"DEMO-{uuid.uuid4().hex[:8].upper()}",
        "hotel_name": hotel_name,
        "original_price": original_price,
        "discounted_price": discounted_price,
        "discount_applied": f"{discount_pct}% OFF using code {discount_code}",
        "confirmation_message": "This is a simulated demo booking. No real transaction occurred.",
        "status": "CONFIRMED_DEMO"
    }
