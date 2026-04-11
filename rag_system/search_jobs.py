import json
import os
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load FAISS index
index = faiss.read_index("job_index.faiss")

# Load metadata
with open("job_metadata.json", "r") as f:
    jobs = json.load(f)


def search(query, top_k=5):
    # Convert query to embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = np.array(
        [response.data[0].embedding]
    ).astype("float32")

    # Search
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        results.append(jobs[i])

    return results


if __name__ == "__main__":
    user_query = input("Enter job search query: ")

    results = search(user_query)

    print("\n=== TOP MATCHES (RAG) ===\n")

    for job in results:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Apply: {job['url']}")
        print("-" * 50)