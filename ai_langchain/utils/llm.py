from openai import OpenAI
import os

def get_llm():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
