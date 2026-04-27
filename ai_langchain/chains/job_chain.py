from langchain_openai import ChatOpenAI


class JobChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            model="gpt-4o-mini"
        )

    def run(self, skills):

        prompt = f"""
        Given these skills:
        {skills}

        Suggest relevant software engineering jobs.

        Return as a simple list of job roles with short descriptions.
        """

        response = self.llm.invoke(prompt)

        content = response.content

        # basic parsing fallback
        jobs = [
            {"title": line.strip(), "description": line.strip()}
            for line in content.split("\n") if line.strip()
        ]

        return {
            "jobs": jobs
        }


def get_job_chain():
    return JobChain()