from langchain_openai import ChatOpenAI


class AdvisorChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            model="gpt-4o-mini"
        )

    def run(self, resume, jobs, skills):

        prompt = f"""
        You are a career advisor AI.

        Resume:
        {resume}

        Skills:
        {skills}

        Jobs:
        {jobs}

        Provide:
        - Career recommendations
        - Skill improvements
        - Best job path
        - Summary
        """

        response = self.llm.invoke(prompt)

        return {
            "recommendations": [response.content],
            "summary": response.content
        }


def get_advisor_chain():
    return AdvisorChain()