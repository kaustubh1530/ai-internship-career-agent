import json
import os
import sys

# ==============================
# FIX PROJECT ROOT PATH
# ==============================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.job_data_source import load_jobs
from backend.embedding_utils import get_embedding


OUTPUT_FILE = os.path.join(PROJECT_ROOT, "backend", "job_embeddings.json")


def build_job_text(job):
    """
    Build clean searchable text for each job.
    """

    title = job.get("title", "")
    company = job.get("company", "")
    location = job.get("location", "")
    description = job.get("description", "")

    return f"{title}\n{company}\n{location}\n{description}"


def build_embeddings():
    """
    Build embeddings for all jobs in data/live_jobs.json
    and save them to backend/job_embeddings.json.
    """

    jobs = load_jobs()

    if not jobs:
        print("No jobs found in data/live_jobs.json")
        return []

    embedded_jobs = []

    for index, job in enumerate(jobs, start=1):
        job_text = build_job_text(job)

        print(f"Processing {index}/{len(jobs)}: {job.get('title', 'Untitled Job')}")

        job["embedding"] = get_embedding(job_text)
        embedded_jobs.append(job)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(embedded_jobs, file, indent=2)

    print(f"✅ Saved {len(embedded_jobs)} embedded jobs to {OUTPUT_FILE}")

    return embedded_jobs


if __name__ == "__main__":
    build_embeddings()