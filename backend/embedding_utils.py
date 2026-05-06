from openai import OpenAI
import numpy as np


client = OpenAI()


def get_embedding(text: str):
    """
    Convert text into an embedding vector using OpenAI embeddings.
    """
    if not text or not text.strip():
        text = "empty"

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