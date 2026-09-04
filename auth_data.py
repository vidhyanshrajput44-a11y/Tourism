import time
import uuid

# In-memory user store for demo purposes
users_db = {}
# OTP storage: phone_number -> {"otp": str, "expires_at": float}
otp_store = {}

def get_user_by_id(user_id):
    return users_db.get(user_id)

def get_user_by_phone(phone_number):
    for u in users_db.values():
        if u.get("phone_number") == phone_number:
            return u
    return None

def get_user_by_email(email):
    for u in users_db.values():
        if u.get("email") == email:
            return u
    return None

def create_user(name, auth_method, phone_number=None, email=None):
    user_id = "usr_" + uuid.uuid4().hex[:8]
    user = {
        "user_id": user_id,
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "auth_method": auth_method,
        "created_at": time.time(),
        "last_login": time.time()
    }
    users_db[user_id] = user
    return user

def update_last_login(user_id):
    if user_id in users_db:
        users_db[user_id]["last_login"] = time.time()
