from typing import Callable
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from backend.services import job_service

app = FastAPI()

class JobsResponse(BaseModel):
    role: str
    location: str
    jobs: list

def get_job_service():
    return job_service.get_jobs


@app.get("/jobs", response_model=JobsResponse)
def get_jobs(
    role: str = Query(
        "software engineering intern",
        min_length=2
    ),
    location: str = "Maryland",
    job_service_func: Callable = Depends(get_job_service)
):
    try:
        jobs = job_service_func(
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