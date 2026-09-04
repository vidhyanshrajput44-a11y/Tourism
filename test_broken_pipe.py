import asyncio
from pydantic import BaseModel
from typing import List, Optional
from chatbot_api import api_chat_message, MessageInput

async def main():
    try:
        input_data = MessageInput(
            user_query="Is it safe to visit Varanasi Ghats right now?",
            conversation_id="test1",
            conversation_history=[]
        )
        print("Sending message...")
        res = api_chat_message(input_data)
        print("Success:", res)
    except Exception as e:
        print("Error:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
