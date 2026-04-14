from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# RESUME AGENT
# =========================
def resume_agent(user_skills):

    prompt = f"""
    You are a Resume Analysis AI.

    Given user skills:
    {", ".join(user_skills)}

    Return:
    1. Top strengths (max 5)
    2. Missing areas (max 5)

    Format:
    Strengths: ...
    Weaknesses: ...
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# =========================
# JOB AGENT
# =========================
def job_agent(job_text):

    prompt = f"""
    You are a Job Analysis AI.

    Analyze the job description and extract:
    - Required skills
    - Job type (backend / frontend / AI / fullstack)

    Job:
    {job_text[:1500]}

    Keep it short.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# =========================
# ADVISOR AGENT
# =========================
def advisor_agent(user_skills, job_text):

    prompt = f"""
    You are an AI Career Advisor.

    User Skills:
    {", ".join(user_skills)}

    Job Description:
    {job_text[:1500]}

    Task:
    1. Explain why this job matches the user
    2. Suggest 2-3 skills to improve

    Keep it short and practical.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content