with open("api.py", "r") as f:
    code = f.read()

new_router = """
# --- UI 9: Photo-Based Heritage Rewards ---
from heritage_rewards_api import rewards_router
app.include_router(rewards_router)
# ---------------------------------------------------------------------------

# Serve frontend (must be after API routes)
"""

code = code.replace("# Serve frontend (must be after API routes)", new_router.strip())

with open("api.py", "w") as f:
    f.write(code)

print("Patched api.py")
