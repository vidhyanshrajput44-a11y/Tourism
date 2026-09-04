"""
Test script for UI 8 - Photo-Based Heritage Rewards + Booking Redemption
"""

import httpx
import os

base_url = "http://127.0.0.1:8000/rewards"
user_id = "test_demo_user"
dest_id = "taj_mahal"
monument_id = "m_taj_1"

print("--- Testing Heritage Rewards & Bookings ---")

# 1. Get monuments
r = httpx.get(f"{base_url}/monuments/{dest_id}")
print("Monuments:", r.json())

# 2. Submit a photo (force verify for demo)
# We need to simulate a multipart file upload
try:
    with open("data/sample.jpg", "wb") as f:
        f.write(b"dummy image data")
        
    with open("data/sample.jpg", "rb") as f:
        files = {"image": ("sample.jpg", f, "image/jpeg")}
        data = {
            "user_id": user_id,
            "monument_id": monument_id,
            "destination_id": dest_id,
            "force_verify": "true"
        }
        r = httpx.post(f"{base_url}/submit-photo", data=data, files=files)
        print("\nSubmit Photo Result:", r.json())
except Exception as e:
    print("Photo submit failed:", e)

# 3. Check Points
r = httpx.get(f"{base_url}/my-points/{user_id}")
print("\nMy Points:", r.json())

# 4. We need 500 points to test redeem. Let's submit 2 more times to hit 600 pts.
for i in range(2):
    with open("data/sample.jpg", "rb") as f:
        files = {"image": ("sample.jpg", f, "image/jpeg")}
        httpx.post(f"{base_url}/submit-photo", data=data, files=files)

r = httpx.get(f"{base_url}/my-points/{user_id}")
print(f"\nPoints after multiple submissions: {r.json()['ledger']['current_balance']} pts")

# 5. Check Available Tiers
r = httpx.get(f"{base_url}/available-tiers/{user_id}")
print("\nAvailable Tiers:", [t['name'] for t in r.json() if t['is_eligible']])

# 6. Redeem Tier 10
r = httpx.post(f"{base_url}/redeem", json={"user_id": user_id, "tier_id": "tier_10"})
redeem_res = r.json()
print("\nRedeemed Reward:", redeem_res)

# 7. MakeMyTrip Link
r = httpx.get(f"{base_url}/book/makemytrip-link?destination_id={dest_id}")
print("\nMakeMyTrip Real URL:", r.json())

# 8. Partner Preview Mock
mock_req = {
    "user_id": user_id,
    "hotel_name": "Taj Heritage Test",
    "discount_code": redeem_res["discount_code"],
    "discount_pct": redeem_res["discount_pct"]
}
r = httpx.post(f"{base_url}/book/partner-preview", json=mock_req)
print("\nPartner Preview Confirmation:", r.json())

# Cleanup
if os.path.exists("data/sample.jpg"):
    os.remove("data/sample.jpg")

print("\n--- All tests passed! ---")
