from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from rag_engine import get_rag_engine, generate_answer

chat_router = APIRouter(prefix="/chat", tags=["Chatbot"])

class MessageInput(BaseModel):
    user_query: str
    conversation_id: str
    conversation_history: Optional[List[dict]] = []

@chat_router.post("/message")
def api_chat_message(input_data: MessageInput):
    if not input_data.user_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        import time
        t0 = time.time()
        rag = get_rag_engine()
        t1 = time.time()
        print(f"[PROFILER] get_rag_engine: {t1-t0:.3f}s")
        result = generate_answer(rag, input_data.user_query, input_data.conversation_history)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chat_router.post("/refresh-knowledge-base")
def api_refresh_kb(background_tasks: BackgroundTasks):
    try:
        import threading
        rag = get_rag_engine()
        # Run explicitly in a separate daemon thread to completely decouple from FastAPI's event loop and thread pool
        threading.Thread(target=rag.refresh, daemon=True).start()
        return {"status": "success", "message": "Knowledge base refresh triggered in background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chat_router.get("/sample-questions")
def api_sample_questions():
    # Curated questions to demonstrate RAG capability
    return [
        "Best time to visit Jaipur City Palace?",
        "Is it safe to visit Varanasi Ghats right now?",
        "Suggest a less crowded alternative to Goa Baga Beach.",
        "Are there any hotels available near Hampi?",
        "Tell me about local markets near the Taj Mahal."
    ]
