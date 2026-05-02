from langchain_openai import ChatOpenAI
from ai_langchain.prompts.advisor_prompt import advisor_prompt


class AdvisorChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            model="gpt-4o-mini"
        )

    def run(self, resume, jobs, skills, history):

        # FORMAT INPUTS CLEANLY
        jobs_text = "\n\n".join([
            f"- {job.get('title')} at {job.get('company')} ({job.get('location')})"
            for job in jobs
        ]) if jobs else "No jobs available"

        history_text = "\n".join([
            f"Past Skills: {h.get('skills')}, Jobs: {h.get('top_jobs')}"
            for h in history
        ]) if history else "No past history"

        skills_text = ", ".join(skills) if skills else "No skills extracted"

        # BUILD PROMPT
        prompt = advisor_prompt.format(
            resume=resume,
            jobs=jobs_text,
            skills=skills_text,
            history=history_text
        )

        # LLM CALL
        response = self.llm.invoke(prompt)

        # RETURN STRUCTURED OUTPUT
        return {
            "recommendations": [response.content],
            "summary": response.content
        }


def get_advisor_chain():
    return AdvisorChain()