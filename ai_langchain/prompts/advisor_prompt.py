from langchain_core.prompts import PromptTemplate
advisor_prompt = PromptTemplate(
    input_variables=["user_skills", "job_text"],
    template="""
You are an AI Career Advisor.

User Skills:
{user_skills}

Job Description:
{job_text}

Task:
1. Explain why this job matches the user
2. Suggest 2-3 skills to improve

Keep it short and practical.
"""
)
