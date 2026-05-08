import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

load_dotenv()


def get_openai_client():
    """
    Create OpenAI client using OPENAI_API_KEY from:
    - local .env
    - local .streamlit/secrets.toml root-level env
    - Streamlit Cloud secrets root-level env
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing OPENAI_API_KEY. Add it to .env locally or Streamlit Secrets in deployment."
        )

    return OpenAI(api_key=api_key)


def get_embedding(text: str):
    """
    Convert text into an embedding vector using OpenAI embeddings.
    """
    if not text or not text.strip():
        text = "empty"

    client = get_openai_client()

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:8000]
    )

    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """
    Compare two embedding vectors and return similarity score.
    Higher score = more similar.
    """
    if not vec1 or not vec2:
        return 0.0

    v1 = np.array(vec1)
    v2 = np.array(vec2)

    denominator = np.linalg.norm(v1) * np.linalg.norm(v2)

    if denominator == 0:
        return 0.0

    return float(np.dot(v1, v2) / denominator)