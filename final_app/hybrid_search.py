# final_app/hybrid_search.py

import numpy as np
from backend.search_jobs import load_or_create_index, get_embedding


def skill_match_score(job_text, user_skills):
    job_text = job_text.lower()
    matched = [s for s in user_skills if s.lower() in job_text]
    score = len(matched) / max(len(user_skills), 1)
    return score, matched


def hybrid_search(query, user_skills, top_k=5):

    index, jobs = load_or_create_index()

    query_embedding = np.array(
        [get_embedding(query)]
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k * 2)

    results = []

    for idx, i in enumerate(indices[0]):
        job = jobs[i]

        job_text = f"{job.get('title', '')} {job.get('description', '')}"

        skill_score, matched = skill_match_score(job_text, user_skills)

        rag_score = 1 / (1 + distances[0][idx])

        final_score = (0.7 * rag_score) + (0.3 * skill_score)

        results.append({
            "job": job,
            "score": round(final_score * 100, 2),
            "matched": matched
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]
