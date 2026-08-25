from fastapi import FastAPI
from backend.live_job_fetcher import fetch_live_jobs

app = FastAPI()


@app.get("/jobs")
def get_jobs(
    role: str = "software engineering intern",
    location: str = "Maryland"
):
    jobs = fetch_live_jobs(
        role=role,
        location=location
    )

    return {
        "role": role,
        "location": location,
        "jobs": jobs
    }
