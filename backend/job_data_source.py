import json
import os


DATA_FILE = "data/live_jobs.json"


def load_jobs():
    """
    Load jobs from data/live_jobs.json.
    Returns an empty list if the file does not exist or is invalid.
    """

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            jobs = json.load(file)

        if not isinstance(jobs, list):
            return []

        return jobs

    except json.JSONDecodeError:
        return []