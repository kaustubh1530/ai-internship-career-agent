from ai_langchain.utils.llm import get_llm
import json


class ResumeChain:
    def run(self, resume_text):

        client = get_llm()

        prompt = f"""
Extract skills from this resume.

Return ONLY a JSON list:
["Python", "FastAPI", "AI"]

Resume:
{resume_text}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        try:
            skills = json.loads(content)
        except:
            skills = []

        return {"skills": skills}


def get_resume_chain():
    return ResumeChain()
