import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

DATA_FILE = "data/live_jobs.json"


def get_secret(key: str):
    """
    Read secrets safely from environment variables.
    Streamlit Cloud root-level secrets are also available as environment variables.
    """
    value = os.getenv(key)

    if value:
        return value

    return None


def normalize_job(raw_job):
    """
    Convert raw Adzuna API job data into the clean format our app expects.
    """
    title = raw_job.get("title", "Untitled Job")
    company = raw_job.get("company", {}).get("display_name", "Unknown Company")
    location = raw_job.get("location", {}).get("display_name", "Unknown Location")
    description = raw_job.get("description", "")
    url = raw_job.get("redirect_url", "#")

    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "url": url
    }


def fetch_live_jobs(
    role="software engineering intern",
    location="Maryland",
    results_per_page=20
):
    """
    Fetch fresh jobs from Adzuna and save them to data/live_jobs.json.
    """
    app_id = get_secret("ADZUNA_APP_ID")
    app_key = get_secret("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError(
            "Missing ADZUNA_APP_ID or ADZUNA_APP_KEY. Add them to .env locally or Streamlit Secrets in deployment."
        )

    role = role or "software engineering intern"
    location = location or "Maryland"

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": role,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(
            f"Job API request failed: {response.status_code} - {response.text}"
        )

    data = response.json()
    raw_jobs = data.get("results", [])

    jobs = [normalize_job(job) for job in raw_jobs]

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=2)

    return jobs


if __name__ == "__main__":
    jobs = fetch_live_jobs()
    print(f"✅ Saved {len(jobs)} jobs to {DATA_FILE}")