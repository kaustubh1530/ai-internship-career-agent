from langchain.tools import Tool

from backend.agents import resume_agent, advisor_agent
from backend.search_jobs import search_jobs

from ai_langchain.context import (
    get_user_skills,
    set_jobs,
    get_jobs
)


# =========================
# RESUME TOOL
# =========================
def resume_tool_func(_):
    skills = get_user_skills()

    if not skills:
        return "No user skills available."

    return resume_agent(skills)


# =========================
# JOB SEARCH TOOL
# =========================
def job_search_tool_func(query):
    jobs = search_jobs(query)

    set_jobs(jobs)

    return f"Found {len(jobs)} jobs"


# =========================
# ADVISOR TOOL
# =========================
def advisor_tool_func(_):
    skills = get_user_skills()
    jobs = get_jobs()

    if not skills or not jobs:
        return "Missing data for advice."

    job_text = jobs[0].get("description", "")

    return advisor_agent(skills, job_text)


# =========================
# TOOL LIST
# =========================
def get_tools():

    tools = [
        Tool(
            name="Resume Analyzer",
            func=resume_tool_func,
            description="Analyze the user's resume skills"
        ),
        Tool(
            name="Job Search",
            func=job_search_tool_func,
            description="Search for jobs ONCE based on a query. Do NOT call this multiple times."
        ),
        Tool(
            name="Career Advisor",
            func=advisor_tool_func,
            description="Give career advice using resume and job data"
        )
    ]

    return tools