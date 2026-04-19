from langchain_core.prompts import PromptTemplate

job_prompt = PromptTemplate(
    input_variables=["job_text"],
    template="""
You are a Job Analysis AI.

Analyze the job description and extract:
- Required skills
- Job type (backend / frontend / AI / fullstack)

Job:
{job_text}

Keep it short.
"""
)
