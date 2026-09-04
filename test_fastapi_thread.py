import os
# os.environ["TOKENIZERS_PARALLELISM"] = "false" # uncomment to test fix

import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from chatbot_api import chat_router

app = FastAPI()
app.include_router(chat_router)

client = TestClient(app)

def run():
    response = client.post("/chat/message", json={
        "user_query": "Is it safe to visit Varanasi Ghats right now?",
        "conversation_id": "test1",
        "conversation_history": []
    })
    print(response.json())

if __name__ == "__main__":
    run()
