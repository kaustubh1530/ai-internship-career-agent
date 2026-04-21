from langchain.tools import Tool
from backend.agents import resume_agent
from ai_langchain.context import get_user_skills


def resume_tool_func(_):
    skills = get_user_skills()
    
    if not skills:
        return "No user skills available."

    return resume_agent(skills)