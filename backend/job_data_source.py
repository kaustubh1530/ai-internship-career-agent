import json
import os


def load_jobs():
    file_path = os.path.join("data", "live_jobs.json")

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        jobs = json.load(f)

    return jobs