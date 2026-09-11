from google import genai
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Add it to your .env file."
    )


client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
you are an ai therapist
"""


def create_chat():
    """
    Creates a new Gemini chat.

    The chat object stores the conversation history in memory.
    """

    chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return chat