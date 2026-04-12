import json
import os
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv

# =========================
# INIT
# =========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "job_index.faiss")
META_PATH = os.path.join(BASE_DIR, "job_metadata.json")

# =========================
# LOAD DATA
# =========================
index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "r") as f:
    jobs = json.load(f)

# =========================
# RAG SEARCH FUNCTION
# =========================
def search(query, top_k=5):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = np.array(
        [response.data[0].embedding]
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i in indices[0]:
        if i < len(jobs):
            job = jobs[i]

            # simple score from FAISS distance
            job["score"] = float(1 / (1 + distances[0][list(indices[0]).index(i)]))

            results.append(job)

    return results


# =========================
# TEST (optional)
# =========================
if __name__ == "__main__":
    q = input("Search: ")
    res = search(q)

    for r in res:
        print(r["title"], r["company"])