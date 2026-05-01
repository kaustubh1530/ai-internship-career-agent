import json
from backend.job_data_source import load_jobs
from backend.embedding_utils import get_embedding


def build_embeddings():
    jobs = load_jobs()

    embedded_jobs = []

    for job in jobs:
        text = job.get("title", "") + " " + job.get("description", "")

        embedding = get_embedding(text)

        job["embedding"] = embedding

        embedded_jobs.append(job)

        print(f"Processed: {job.get('title')}")

    with open("backend/job_embeddings.json", "w") as f:
        json.dump(embedded_jobs, f)

    print("✅ Job embeddings saved!")


if __name__ == "__main__":
    build_embeddings()