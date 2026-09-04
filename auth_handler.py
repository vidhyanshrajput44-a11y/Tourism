import os
import time
import random
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from auth_data import otp_store, get_user_by_phone, get_user_by_email, create_user, update_last_login

JWT_SECRET = os.environ.get("JWT_SECRET", "super-secret-demo-key-123")
JWT_ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "725705714389-mtl0ss6oucr32uug4g76k9fvpsdktcka.apps.googleusercontent.com")

def generate_session_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": time.time() + 86400 # 24 hour expiry
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_session(token: str) -> str:
    """Returns user_id if valid, raises Exception if invalid."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except Exception as e:
        raise ValueError("Invalid or expired session token")

import httpx

FAST2SMS_API_KEY = os.environ.get("FAST2SMS_API_KEY", "SKqTIuHbGPfVBDdZYcpOXeCsjNywmo7vMAgLt9F10z3RWhJ6iaOUfZTdXLM6tni0Ym8KuqV3GFNaBx2P")

def send_real_sms(phone_number: str, otp_code: str):
    """Sends a real SMS using Fast2SMS API if key is present."""
    if not FAST2SMS_API_KEY:
        print(f"\n[DEMO SMS] Sent OTP {otp_code} to {phone_number} (Add FAST2SMS_API_KEY to send real SMS)\n")
        return True
        
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        # Fast2SMS requires 10-digit number without +91
        clean_phone = phone_number.replace("+91", "").replace(" ", "").replace("-", "")
        if len(clean_phone) > 10:
            clean_phone = clean_phone[-10:]
            
        payload = f"variables_values={otp_code}&route=otp&numbers={clean_phone}"
        headers = {
            'authorization': FAST2SMS_API_KEY,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = httpx.post(url, data=payload, headers=headers)
        
        if response.status_code == 200 and response.json().get('return'):
            print(f"✅ Real SMS OTP sent successfully to {clean_phone}")
            return True
        else:
            print(f"❌ Failed to send SMS: {response.text}")
            return False
    except Exception as e:
        print(f"❌ SMS Gateway Error: {e}")
        return False

def request_otp(phone_number: str, name: str = None, email: str = None) -> dict:
    otp_code = str(random.randint(100000, 999999))
    expires_at = time.time() + 300 # 5 minutes
    
    otp_store[phone_number] = {
        "otp": otp_code,
        "expires_at": expires_at,
        "name": name,
        "email": email
    }
    
    # --- DEMO MODE: Simulate sending SMS ---
    print(f"\n[DEMO SMS] Sent OTP {otp_code} to {phone_number}\n")
    
    return {
        "success": True,
        "demo_otp": otp_code, # Always return in demo mode so frontend can show it
        "expires_in_seconds": 300
    }

def verify_otp(phone_number: str, otp_code: str) -> dict:
    record = otp_store.get(phone_number)
    if not record:
        raise ValueError("No OTP requested for this number")
    
    if time.time() > record["expires_at"]:
        raise ValueError("OTP expired")
        
    if record["otp"] != otp_code:
        raise ValueError("Invalid OTP")
        
    # Clear OTP
    del otp_store[phone_number]
    
    user = get_user_by_phone(phone_number)
    if not user:
        r_name = record.get("name") or "Guest User"
        r_email = record.get("email")
        user = create_user(name=r_name, auth_method="phone", phone_number=phone_number, email=r_email)
    else:
        update_last_login(user["user_id"])
        
    token = generate_session_token(user["user_id"])
    return {"success": True, "session_token": token, "user": user}

def verify_google_token(token: str) -> dict:
    # Basic decoding for demo if no Client ID is provided
    if not GOOGLE_CLIENT_ID:
        try:
            # Unverified decode for DEMO purposes ONLY if no client ID is set
            idinfo = jwt.decode(token, options={"verify_signature": False})
        except Exception:
            raise ValueError("Invalid Google token format")
    else:
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        except ValueError:
            raise ValueError("Invalid Google token")

    email = idinfo.get("email")
    name = idinfo.get("name", "Google User")
    
    if not email:
        raise ValueError("Email not provided by Google")
        
    user = get_user_by_email(email)
    if not user:
        user = create_user(name=name, auth_method="google", email=email)
    else:
        update_last_login(user["user_id"])
        
    session_token = generate_session_token(user["user_id"])
    return {"success": True, "session_token": session_token, "user": user}
