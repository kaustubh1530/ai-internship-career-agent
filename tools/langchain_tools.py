from langchain.tools import Tool
from backend.agents import resume_agent, job_agent, advisor_agent


def get_tools():

    tools = [
        Tool(
            name="Resume Analyzer",
            func=lambda x: resume_agent(x.split(",")),
            description="Analyze user skills and return strengths and weaknesses"
        ),
        Tool(
            name="Job Analyzer",
            func=job_agent,
            description="Analyze a job description and extract skills and job type"
        ),
        Tool(
            name="Career Advisor",
            func=lambda x: advisor_agent(x.split(","), ""),
            description="Give career advice based on user skills"
        )
    ]

    return tools