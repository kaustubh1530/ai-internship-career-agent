import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_jobs():
    with open("data/live_jobs.json", "r") as file:
        return json.load(file)


def search_jobs(user_query):
    jobs = load_jobs()
    matched_jobs = []
    query = user_query.lower()

    for job in jobs:
        title = (job.get("title") or "").lower()
        location = (job.get("location") or "").lower()

        if (
            "intern" in query
            or "software" in query and "software" in title
            or "ai" in query and "ai" in title
            or "backend" in query and "backend" in title
            or any(loc in location for loc in ["maryland", "virginia", "washington"])
        ):
            matched_jobs.append(job)

    return matched_jobs


def extract_skills_from_description(description):
    if not description:
        return []

    prompt = f"""
    Extract technical skills from this job description.
    Return ONLY a Python list like ["python", "sql", "api"].

    Description:
    {description}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract only skills."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("[") and text.endswith("]"):
            skills = eval(text)
            return [s.lower() for s in skills if isinstance(s, str)]

        return fallback_skills(description)

    except:
        return fallback_skills(description)


def fallback_skills(description):
    keywords = [
        "python", "api", "fastapi", "sql", "git",
        "aws", "docker", "machine learning",
        "llm", "rag", "numpy", "pandas"
    ]

    desc = description.lower()
    return [k for k in keywords if k in desc]