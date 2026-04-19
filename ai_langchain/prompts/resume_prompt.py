from langchain_core.prompts import PromptTemplate

resume_prompt = PromptTemplate(
    input_variables=["user_skills"],
    template="""
You are a Resume Analysis AI.

Given user skills:
{user_skills}

Return:
1. Top strengths (max 3)
2. Missing areas (max 3)

Format:
Strengths: ...
Weaknesses: ...
"""
)
