# backend/search_jobs.py

import json
import os
import numpy as np
import faiss
import time
from openai import OpenAI
from dotenv import load_dotenv

from backend.job_api import get_jobs  # 🔥 NEW

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

CACHE_DURATION = 3600  # 1 hour


# =========================
# EMBEDDING FUNCTION
# =========================
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# =========================
# CHECK INDEX VALIDITY
# =========================
def is_index_valid():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        return False

    last_modified = os.path.getmtime(INDEX_PATH)
    return (time.time() - last_modified) < CACHE_DURATION


# =========================
# BUILD INDEX FROM JOBS
# =========================
def build_index(jobs):
    print("🔥 Building new FAISS index...")

    embeddings = []

    for job in jobs:
        text = f"{job.get('title', '')} {job.get('description', '')}"
        emb = get_embedding(text)
        embeddings.append(emb)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w") as f:
        json.dump(jobs, f, indent=2)

    return index, jobs


# =========================
# LOAD OR BUILD INDEX
# =========================
def load_or_create_index():
    if is_index_valid():
        print("⚡ Using cached FAISS index")
        index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "r") as f:
            jobs = json.load(f)

        return index, jobs

    else:
        jobs = get_jobs()  # 🔥 fetch fresh jobs
        return build_index(jobs)


# =========================
# SEARCH FUNCTION
# =========================
def search(query, top_k=5):

    index, jobs = load_or_create_index()

    query_embedding = np.array(
        [get_embedding(query)]
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx, i in enumerate(indices[0]):
        if i < len(jobs):
            job = jobs[i]

            score = float(1 / (1 + distances[0][idx]))

            job["score"] = round(score * 100, 2)

            results.append(job)

    return results


# =========================
# TEST
# =========================
if __name__ == "__main__":
    q = input("Search: ")
    res = search(q)

    for r in res:
        print(r["title"], r.get("company", ""))
