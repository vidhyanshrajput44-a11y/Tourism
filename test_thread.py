import concurrent.futures
from chatbot_api import api_chat_message, MessageInput

def run_in_thread():
    input_data = MessageInput(
        user_query="Is it safe to visit Varanasi Ghats right now?",
        conversation_id="test1",
        conversation_history=[]
    )
    try:
        res = api_chat_message(input_data)
        print("Success:", res)
    except Exception as e:
        print("Error in thread:", repr(e))

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(run_in_thread)
        future.result()
