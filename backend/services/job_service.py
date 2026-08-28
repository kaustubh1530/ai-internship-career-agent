from backend.live_job_fetcher import fetch_live_jobs


def get_jobs(role: str, location: str):
    return fetch_live_jobs(
        role=role,
        location=location
    )