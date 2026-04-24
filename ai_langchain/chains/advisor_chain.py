from ai_langchain.utils.llm import get_llm
import json


class AdvisorChain:
    def run(self, resume, jobs):

        client = get_llm()

        prompt = f"""
You are a career advisor.

Resume:
{resume}

Jobs:
{jobs}

Return JSON:
{{
  "recommendations": ["improve Python", "learn system design"],
  "summary": "short advice"
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        try:
            result = json.loads(content)
        except:
            result = {"recommendations": [], "summary": content}

        return result


def get_advisor_chain():
    return AdvisorChain()
