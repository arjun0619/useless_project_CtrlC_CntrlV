from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is not set. Add it to your .env file."
    )


client = Groq(api_key=api_key)


SYSTEM_PROMPT = """
you are an ai therapist
"""


def create_chat():
    """
    Creates a new Groq conversation.

    The chat object stores the conversation history in memory.
    """

    return [{"role": "system", "content": SYSTEM_PROMPT}]
