import httpx

def test_auth():
    print("--- Testing UI 8: Authentication API ---\n")
    base_url = "http://127.0.0.1:8000"
    
    test_phone = "+919999911111"
    
    print("[1] Requesting OTP (Signup)...")
    try:
        r = httpx.post(f"{base_url}/auth/otp/request", json={
            "phone_number": test_phone,
            "name": "Vidhyansh",
            "email": "vidh@example.com",
            "is_signup": True
        })
        res = r.json()
        print(f"  Response: {res}")
        demo_otp = res.get("demo_otp")
        if not demo_otp:
            print("  FAIL: No DEMO OTP returned")
            return
    except Exception as e:
        print(f"  Error: {e}")
        return
    print()

    print(f"[2] Verifying OTP ({demo_otp})...")
    session_token = None
    try:
        r = httpx.post(f"{base_url}/auth/otp/verify", json={"phone_number": test_phone, "otp_code": demo_otp})
        res = r.json()
        print(f"  Response: {res}")
        session_token = res.get("session_token")
        if not session_token:
            print("  FAIL: No session token returned")
            return
    except Exception as e:
        print(f"  Error: {e}")
        return
    print()

    print("[3] Testing /auth/me with Session Token...")
    try:
        r = httpx.get(
            f"{base_url}/auth/me",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        res = r.json()
        print(f"  Response: {res}")
        if res.get("success") and res.get("user"):
            print("  ✅ PASS: Authentication pipeline works!")
        else:
            print("  FAIL: User not authenticated properly")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_auth()
