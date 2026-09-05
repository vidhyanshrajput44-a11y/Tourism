import json
import os

# Disable tokenizers parallelism to fix [Errno 32] Broken pipe on MacOS with FastAPI
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from knowledge_builder import build_knowledge_base

class RAGEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print("Initializing RAG Engine...")
        self.encoder = SentenceTransformer(model_name)
        self.documents = []
        self.index = None
        self.load_knowledge_base()

    def load_knowledge_base(self):
        kb_exists = os.path.exists("knowledge_base.json")
        index_exists = os.path.exists("faiss_index.bin")
        
        if not kb_exists:
            self.documents = build_knowledge_base()
        else:
            with open("knowledge_base.json", "r") as f:
                self.documents = json.load(f)
        
        if not self.documents:
            print("Warning: Knowledge base is empty.")
            return

        if index_exists and kb_exists:
            print("Loading FAISS index from disk...")
            self.index = faiss.read_index("faiss_index.bin")
        else:
            print("Embedding documents for FAISS index...")
            texts = [doc["text"] for doc in self.documents]
            embeddings = self.encoder.encode(texts, convert_to_numpy=True)
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
            faiss.write_index(self.index, "faiss_index.bin")
            print("FAISS index built and saved successfully.")

    def refresh(self):
        self.documents = build_knowledge_base()
        if self.documents:
            texts = [doc["text"] for doc in self.documents]
            embeddings = self.encoder.encode(texts, convert_to_numpy=True)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)
            faiss.write_index(self.index, "faiss_index.bin")

    def retrieve_context(self, user_query, top_k=3):
        if not self.index:
            return []
        
        query_vector = self.encoder.encode([user_query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vector, top_k)
        
        retrieved_docs = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.documents):
                retrieved_docs.append(self.documents[idx])
        return retrieved_docs

def call_llm(prompt):
    """
    Swappable LLM integration. Tries to use google.generativeai if API key is present.
    Otherwise falls back to a simple heuristic response.
    """
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            # Limit tokens to force short/fast responses, since tourist questions usually need concise answers
            generation_config = genai.types.GenerationConfig(max_output_tokens=150, temperature=0.3)
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            print("LLM Error:", e)
            return f"I'm experiencing connectivity issues with my AI brain. Error: {e}"
    else:
        # Graceful fallback for demo if no API key is provided
        # Extract the context from the prompt (it's between CONTEXT: and USER QUERY:)
        try:
            ctx_start = prompt.find("CONTEXT:\n") + 9
            ctx_end = prompt.find("\n\nUSER QUERY:")
            context = prompt[ctx_start:ctx_end].strip()
            return f"Based on my data:\n{context}"
        except:
            return "I don't have enough context or an active LLM connection to answer that right now."

def generate_answer(rag_engine, user_query, conversation_history=None):
    import time
    t0 = time.time()
    
    docs = rag_engine.retrieve_context(user_query, top_k=3)
    t1 = time.time()
    
    context_text = "\n".join([f"- {d['text']}" for d in docs])
    sources_used = list(set([d["source_module"] for d in docs]))
    
    system_prompt = (
        "You are 'FootPrint Assistant', a helpful tourist guide AI. "
        "Your goal is to answer the user's question using ONLY the provided context below. "
        "Do not hallucinate. If the context does not contain the answer, say 'I don't have that information in my current data.' "
        "Keep answers concise, friendly, and formatted nicely (use bullet points if listing options). "
    )
    
    hist_text = ""
    if conversation_history:
        for msg in conversation_history[-3:]: # last 3 turns
            role = msg.get("role", "user")
            hist_text += f"{role.upper()}: {msg.get('content')}\n"
    
    full_prompt = f"{system_prompt}\n\nCONTEXT:\n{context_text}\n\nHISTORY:\n{hist_text}\n\nUSER QUERY:\n{user_query}\n\nANSWER:"
    
    t2 = time.time()
    answer = call_llm(full_prompt)
    t3 = time.time()
    
    print(f"[PROFILER] FAISS Retrieve: {t1-t0:.3f}s")
    print(f"[PROFILER] Prompt prep: {t2-t1:.3f}s")
    print(f"[PROFILER] LLM Call: {t3-t2:.3f}s")
    print(f"[PROFILER] Total generate_answer: {t3-t0:.3f}s")
    
    return {
        "answer": answer,
        "sources_used": sources_used,
        "suggested_followups": [
            "What are the nearest hotels?",
            "Are there any safety alerts?",
            "Tell me about local markets."
        ]
    }

# Global instance
rag_engine = None
def get_rag_engine():
    global rag_engine
    if rag_engine is None:
        rag_engine = RAGEngine()
    return rag_engine
