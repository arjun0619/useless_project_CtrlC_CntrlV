from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from character import message
import os



# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is not set. Add it to your .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(api_key=api_key)




SYSTEM_PROMPT = message  # Use the message from character.py as the system prompt


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Therapist",
    description="A casual AI therapist powered by Groq",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




conversations = {}



class ChatRequest(BaseModel):
    session_id: str
    message: str


class NewChatRequest(BaseModel):
    session_id: str



def create_chat():
    """
    Create a new Groq conversation.

    The conversation keeps the previous messages in memory,
    allowing the AI to remember what was said during the
    current session.
    """

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Therapist API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ============================================================
# START NEW SESSION
# ============================================================

@app.post("/new-chat")
def new_chat(request: NewChatRequest):

    chat = create_chat()

    conversations[request.session_id] = chat

    return {
        "success": True,
        "session_id": request.session_id
    }



@app.post("/chat")
def chat(request: ChatRequest):

    session_id = request.session_id
    user_message = request.message.strip()



    if not user_message:
        return {
            "success": False,
            "error": "Message cannot be empty."
        }

    
    if session_id not in conversations:
        conversations[session_id] = create_chat()

    chat = conversations[session_id]

  

    try:

        chat.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=chat,
            temperature=1.0,
            max_completion_tokens=1024,
            reasoning_effort="medium",
        )
        reply = response.choices[0].message.content or ""
        chat.append({"role": "assistant", "content": reply})

        return {
            "success": True,
            "reply": reply
        }

    except Exception as e:

        print("Groq error:", e)

        return {
            "success": False,
            "error": "Something went wrong while talking to the AI."
        }




@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):

    if session_id in conversations:
        del conversations[session_id]

    return {
        "success": True,
        "message": "Chat memory deleted."
    }



if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
