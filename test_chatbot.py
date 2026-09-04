import httpx
import time

def run_tests():
    print("--- Testing UI 7: RAG Chatbot API ---\n")
    base_url = "http://127.0.0.1:8000"
    
    print("[1] Syncing Knowledge Base...")
    try:
        r = httpx.post(f"{base_url}/chat/refresh-knowledge-base")
        print(f"  Response: {r.json()}")
        time.sleep(2) # Give it a moment to build the KB in the background
    except Exception as e:
        print(f"  Error: {e}")
    print()

    print("[2] Fetching Sample Questions...")
    questions = []
    try:
        r = httpx.get(f"{base_url}/chat/sample-questions")
        questions = r.json()
        for q in questions:
            print(f"  - {q}")
    except Exception as e:
        print(f"  Error: {e}")
    print()

    print("[3] Testing RAG Pipeline with Sample Questions...")
    # Test a couple of questions
    for q in questions[:3]:
        print(f"\nQ: {q}")
        try:
            r = httpx.post(
                f"{base_url}/chat/message",
                json={
                    "user_query": q,
                    "conversation_id": "test_123",
                    "conversation_history": []
                },
                timeout=15.0
            )
            res = r.json()
            print(f"A: {res.get('answer')}")
            print(f"Sources Used: {res.get('sources_used')}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    run_tests()
