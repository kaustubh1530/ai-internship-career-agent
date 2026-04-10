import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_jobs():
    with open("data/live_jobs.json", "r") as f:
        return json.load(f)


def search_jobs(query):
    jobs = load_jobs()
    query = query.lower()

    results = []

    for job in jobs:
        title = (job.get("title") or "").lower()
        location = (job.get("location") or "").lower()

        if any(word in title for word in query.split()) or any(
            loc in location for loc in ["maryland", "virginia", "washington", "dc"]
        ):
            results.append(job)

    return results


def extract_skills_from_description(description):
    if not description:
        return []

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract ONLY technical skills from job descriptions. "
                        "Return comma-separated values only. No explanations."
                    )
                },
                {
                    "role": "user",
                    "content": description[:2000]
                }
            ],
            temperature=0
        )

        text = response.choices[0].message.content

        skills = text.replace("\n", ",").split(",")

        cleaned = [
            s.strip().lower()
            for s in skills
            if s.strip() and 1 < len(s.strip()) < 30
        ]

        return list(set(cleaned))

    except Exception as e:
        print("Skill extraction failed:", e)
        return fallback_skills(description)


def fallback_skills(description):
    keywords = [
        "python", "sql", "api", "fastapi",
        "git", "aws", "docker",
        "machine learning", "data",
        "communication"
    ]

    desc = description.lower()

    return [k for k in keywords if k in desc]