from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Add it to your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# ============================================================
# AI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI therapist designed for a fun, casual Gen Z audience.

Your personality:
- Casual
- Friendly
- Slightly blunt
- Funny when appropriate
- Not overly professional
- Simple language
- Never sound like a boring textbook therapist

Your responses should usually be short, around 1 to 3 sentences.

When someone shares a problem:
1. Understand what they are saying.
2. Respond empathetically.
3. Give a short practical suggestion when useful.
4. Keep the conversation natural.
5. Ask a simple follow-up question when appropriate.

You can use light humor, but never make fun of someone's serious suffering.

You are NOT a replacement for a professional mental health provider.

If someone appears to be in immediate danger, seriously injured, or at risk of harming themselves or someone else:
- Take the situation seriously.
- Encourage them to contact local emergency services or a trusted person nearby.
- Encourage professional help.
- Do not make jokes about the situation.

Do not claim to be a real human therapist.

Remember details from earlier messages in the current conversation and use them naturally.
"""


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Therapist",
    description="A casual AI therapist powered by Gemini",
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


# ============================================================
# TEMPORARY CHAT MEMORY
# ============================================================

# This dictionary stores chats in RAM.
#
# Example:
#
# conversations = {
#     "abc123": GeminiChatObject,
#     "xyz456": GeminiChatObject
# }
#
# Because this is only stored in RAM:
#
#   Browser reload      -> frontend can create a new session
#   Server restart      -> memory disappears
#   Computer restart   -> memory disappears
#
# No database is required.

conversations = {}


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):
    session_id: str
    message: str


class NewChatRequest(BaseModel):
    session_id: str


# ============================================================
# CREATE NEW CHAT
# ============================================================

def create_chat():
    """
    Create a new Gemini conversation.

    The conversation keeps the previous messages in memory,
    allowing the AI to remember what was said during the
    current session.
    """

    chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 1.0,
            "max_output_tokens": 150,
        }
    )

    return chat


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


# ============================================================
# SEND MESSAGE
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    session_id = request.session_id
    user_message = request.message.strip()

    # --------------------------------------------------------
    # Validate message
    # --------------------------------------------------------

    if not user_message:
        return {
            "success": False,
            "error": "Message cannot be empty."
        }

    # --------------------------------------------------------
    # Get existing chat
    # --------------------------------------------------------

    if session_id not in conversations:
        conversations[session_id] = create_chat()

    chat = conversations[session_id]

    # --------------------------------------------------------
    # Send message to Gemini
    # --------------------------------------------------------

    try:

        response = chat.send_message(user_message)

        return {
            "success": True,
            "reply": response.text
        }

    except Exception as e:

        print("Gemini error:", e)

        return {
            "success": False,
            "error": "Something went wrong while talking to the AI."
        }


# ============================================================
# DELETE CURRENT CHAT
# ============================================================

@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):

    if session_id in conversations:
        del conversations[session_id]

    return {
        "success": True,
        "message": "Chat memory deleted."
    }


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )