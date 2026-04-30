from openai import OpenAI
import numpy as np

client = OpenAI()


def get_embedding(text: str):
    """
    Convert text → embedding vector
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """
    Compute similarity between 2 vectors
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))