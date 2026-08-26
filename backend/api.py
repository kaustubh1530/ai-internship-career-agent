from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from backend.live_job_fetcher import fetch_live_jobs

app = FastAPI()

class JobsResponse(BaseModel):
    role: str
    location: str
    jobs: list

@app.get("/jobs", response_model=JobsResponse)
def get_jobs(
    role: str = Query(
        "software engineering intern",
        min_length=2
    ),
    location: str = "Maryland"
):
    try:
        jobs = fetch_live_jobs(
            role=role,
            location=location
        )
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Job service is temporarily unavailable"
        )

    return {
        "role": role,
        "location": location,
        "jobs": jobs
    }