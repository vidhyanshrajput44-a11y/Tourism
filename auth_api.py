from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from auth_handler import request_otp, verify_otp, verify_google_token, verify_session
from auth_data import get_user_by_id

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

class OTPRequest(BaseModel):
    phone_number: str
    name: Optional[str] = None
    email: Optional[str] = None
    is_signup: Optional[bool] = False

class OTPVerify(BaseModel):
    phone_number: str
    otp_code: str

class GoogleVerify(BaseModel):
    id_token: str

@auth_router.post("/otp/request")
def api_request_otp(data: OTPRequest):
    if not data.phone_number:
        raise HTTPException(status_code=400, detail="Phone number required")
    try:
        # If login, check if user exists
        from auth_data import get_user_by_phone
        user = get_user_by_phone(data.phone_number)
        if not data.is_signup and not user:
            raise HTTPException(status_code=404, detail="User not found. Please create an account.")
        if data.is_signup and user:
            raise HTTPException(status_code=400, detail="User already exists. Please log in.")
            
        return request_otp(data.phone_number, data.name, data.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.post("/otp/verify")
def api_verify_otp(data: OTPVerify):
    try:
        return verify_otp(data.phone_number, data.otp_code)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.post("/google/verify")
def api_verify_google(data: GoogleVerify):
    try:
        return verify_google_token(data.id_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/me")
def api_get_me(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.split(" ")[1]
    try:
        user_id = verify_session(token)
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"success": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.post("/logout")
def api_logout():
    # Since we are using stateless JWTs, logout is mostly handled client-side
    # by deleting the token. We return success.
    return {"success": True}
