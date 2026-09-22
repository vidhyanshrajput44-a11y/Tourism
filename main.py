"""
Main entry point for FootPrint API.
Re-exports the FastAPI app from api.py so standard start commands like:
    uvicorn main:app --host 0.0.0.0 --port $PORT
work out-of-the-box on Render, Railway, Heroku, etc.
"""

from api import app

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
