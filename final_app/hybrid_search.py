import json
import os
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load data
index = faiss.read_index("../rag_system/job_index.faiss")

with open("../rag_system/job_metadata.json", "r") as f:
    jobs = json.load(f)


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array([response.data[0].embedding]).astype("float32")


def skill_match_score(job_text, user_skills):
    job_text = job_text.lower()
    matched = [s for s in user_skills if s in job_text]
    score = len(matched) / max(len(user_skills), 1)
    return score, matched


def hybrid_search(query, user_skills, top_k=5):
    query_embedding = get_embedding(query)

    distances, indices = index.search(query_embedding, top_k * 2)

    results = []

    for i in indices[0]:
        job = jobs[i]

        job_text = f"{job['title']} {job.get('description', '')}"

        skill_score, matched = skill_match_score(job_text, user_skills)

        # convert distance to similarity
        rag_score = 1 / (1 + distances[0][list(indices[0]).index(i)])

        final_score = (0.7 * rag_score) + (0.3 * skill_score)

        results.append({
            "job": job,
            "score": round(final_score * 100, 2),
            "matched": matched
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]