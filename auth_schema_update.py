import re

with open("auth_handler.py", "r") as f:
    content = f.read()

# Update request_otp to accept name and email
content = content.replace("def request_otp(phone_number: str) -> dict:", "def request_otp(phone_number: str, name: str = None, email: str = None) -> dict:")
content = content.replace('"expires_at": expires_at', '"expires_at": expires_at,\n        "name": name,\n        "email": email')

# Update verify_otp to use the stored name and email when creating user
verify_find = """    user = get_user_by_phone(phone_number)
    if not user:
        user = create_user(name="Guest User", auth_method="phone", phone_number=phone_number)"""
verify_replace = """    user = get_user_by_phone(phone_number)
    if not user:
        r_name = record.get("name") or "Guest User"
        r_email = record.get("email")
        user = create_user(name=r_name, auth_method="phone", phone_number=phone_number, email=r_email)"""
content = content.replace(verify_find, verify_replace)

with open("auth_handler.py", "w") as f:
    f.write(content)


with open("auth_api.py", "r") as f:
    api_content = f.read()

# Update OTPRequest model
api_find = """class OTPRequest(BaseModel):
    phone_number: str"""
api_replace = """class OTPRequest(BaseModel):
    phone_number: str
    name: Optional[str] = None
    email: Optional[str] = None
    is_signup: Optional[bool] = False"""
api_content = api_content.replace(api_find, api_replace)

# Update api_request_otp
api_req_find = """        return request_otp(data.phone_number)"""
api_req_replace = """        # If login, check if user exists
        from auth_data import get_user_by_phone
        user = get_user_by_phone(data.phone_number)
        if not data.is_signup and not user:
            raise HTTPException(status_code=404, detail="User not found. Please create an account.")
        if data.is_signup and user:
            raise HTTPException(status_code=400, detail="User already exists. Please log in.")
            
        return request_otp(data.phone_number, data.name, data.email)"""
api_content = api_content.replace(api_req_find, api_req_replace)

with open("auth_api.py", "w") as f:
    f.write(api_content)

print("Auth backend updated for signup flow.")
