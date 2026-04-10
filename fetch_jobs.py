import requests
import json

APP_ID = "66d536b0"
APP_KEY = "e8f2a220db88cc355f97cf83a1b0091f"


def fetch_jobs():
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 20,
        "what": "software engineer intern",
        "where": "Maryland",
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    data = response.json()

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "description": job.get("description"),
            "url": job.get("redirect_url")
        })

    with open("data/live_jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ Fetched {len(jobs)} jobs and saved to data/live_jobs.json")


if __name__ == "__main__":
    fetch_jobs()