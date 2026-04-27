from langchain_openai import ChatOpenAI


class ResumeChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            model="gpt-4o-mini"
        )

    def run(self, resume_text: str):

        prompt = f"""
        Extract skills from this resume:

        {resume_text}

        Return ONLY a list of skills.
        """

        response = self.llm.invoke(prompt)

        # Simple parsing (safe fallback)
        skills_text = response.content

        # Convert string → list (basic cleanup)
        skills = [s.strip() for s in skills_text.replace("\n", ",").split(",") if s.strip()]

        return {
            "skills": skills
        }


def get_resume_chain():
    return ResumeChain()