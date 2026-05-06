from langchain_openai import ChatOpenAI


class AdvisorChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            model="gpt-4o-mini"
        )

    def run(self, resume, jobs, skills, history=None):

        # -------------------------
        # 🔥 PERFORMANCE FIXES
        # -------------------------
        resume = (resume or "")[:1500]
        jobs = jobs[:5]
        skills = skills[:20]

        history = history or []
        history = history[-2:]

        # -------------------------
        # FORMAT JOBS
        # -------------------------
        jobs_text = "\n\n".join([
            f"{job.get('title')} at {job.get('company')}"
            for job in jobs
        ])

        # -------------------------
        # FORMAT HISTORY
        # -------------------------
        history_text = "\n".join([
            f"Skills: {h.get('skills')}, Jobs: {h.get('top_jobs')}"
            for h in history
        ]) if history else "No previous history"

        # -------------------------
        # PROMPT
        # -------------------------
        prompt = f"""
You are an expert AI Career Advisor.

USER RESUME:
{resume}

USER SKILLS:
{skills}

TOP JOB MATCHES:
{jobs_text}

PAST HISTORY:
{history_text}

TASK:
1. Recommend best career direction
2. Suggest skill improvements
3. Suggest best job roles
4. Keep response structured and concise

FORMAT:
- Career Recommendations
- Skills to Improve
- Best Job Path
- Summary
"""

        # -------------------------
        # LLM CALL
        # -------------------------
        response = self.llm.invoke(prompt)

        return {
            "recommendations": [response.content],
            "summary": response.content
        }


def get_advisor_chain():
    return AdvisorChain()