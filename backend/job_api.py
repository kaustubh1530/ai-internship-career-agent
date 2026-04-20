import requests
import json
import os
import time

APP_ID = "66d536b0"
APP_KEY = "e8f2a220db88cc355f97cf83a1b0091f"

DATA_FILE = "data/live_jobs.json"
CACHE_DURATION = 3600  # 1 hour


# =========================
# CHECK CACHE VALIDITY
# =========================
def is_cache_valid():
    if not os.path.exists(DATA_FILE):
        return False

    last_modified = os.path.getmtime(DATA_FILE)
    current_time = time.time()

    return (current_time - last_modified) < CACHE_DURATION


# =========================
# LOAD FROM FILE
# =========================
def load_cached_jobs():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# =========================
# SAVE TO FILE
# =========================
def save_jobs(jobs):
    with open(DATA_FILE, "w") as f:
        json.dump(jobs, f, indent=2)


# =========================
# FETCH FROM API
# =========================
def fetch_jobs_from_api():
    print("🔥 Fetching fresh jobs from API...")

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

    print(f"✅ Fetched {len(jobs)} jobs")

    return jobs


# =========================
# MAIN FUNCTION (USE THIS)
# =========================
def get_jobs():
    if is_cache_valid():
        print("⚡ Using cached jobs")
        return load_cached_jobs()
    else:
        jobs = fetch_jobs_from_api()
        save_jobs(jobs)
        return jobs


# =========================
# MANUAL TEST
# =========================
if __name__ == "__main__":
    jobs = get_jobs()
    print(f"Total jobs: {len(jobs)}")
