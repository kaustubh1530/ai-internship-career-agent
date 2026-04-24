from ai_langchain.utils.llm import get_llm
import json


class JobChain:
    def run(self, skills):

        client = get_llm()

        prompt = f"""
Match jobs for these skills:
{skills}

Return ONLY JSON:
[
  {{
    "title": "Software Engineer Intern",
    "company": "Google",
    "match_score": 90
  }}
]
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        try:
            jobs = json.loads(content)
        except:
            jobs = []

        return {"jobs": jobs}


def get_job_chain():
    return JobChain()
