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
# JOB SEARCH TOOL (FIXED 🔥)
# =========================
def job_search_tool_func(query):
    jobs = search_jobs(query)

    if not jobs:
        return "No jobs found."

    # Store jobs in shared context
    set_jobs(jobs)

    # Return detailed job info (IMPORTANT)
    result = ""

    for job in jobs[:5]:  # limit to top 5
        result += f"""
Title: {job.get('title', 'N/A')}
Company: {job.get('company', 'N/A')}
Location: {job.get('location', 'N/A')}
Description: {job.get('description', '')[:200]}
Apply Link: {job.get('url', 'N/A')}

------------------------
"""

    return result


# =========================
# ADVISOR TOOL (IMPROVED 🔥)
# =========================
def advisor_tool_func(_):
    skills = get_user_skills()
    jobs = get_jobs()

    if not skills:
        return "No user skills available."

    if not jobs:
        return "No job data available. Please search for jobs first."

    # Combine top jobs into one text
    combined_jobs = ""

    for job in jobs[:3]:  # use top 3 jobs
        combined_jobs += f"""
Title: {job.get('title')}
Description: {job.get('description', '')[:300]}

"""

    return advisor_agent(skills, combined_jobs)


# =========================
# TOOL LIST
# =========================
def get_tools():

    tools = [
        Tool(
            name="Resume Analyzer",
            func=resume_tool_func,
            description="Analyze the user's resume skills and identify strengths and weaknesses."
        ),
        Tool(
            name="Job Search",
            func=job_search_tool_func,
            description="Search for jobs based on a role or query and return detailed job listings. Use this when the user asks for jobs."
        ),
        Tool(
            name="Career Advisor",
            func=advisor_tool_func,
            description="Give career advice by comparing user skills with job requirements. Use this after job search."
        )
    ]

    return tools