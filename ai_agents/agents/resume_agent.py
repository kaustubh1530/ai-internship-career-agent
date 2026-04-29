from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.resume_chain import get_resume_chain


class ResumeAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResumeAgent")

    def run(self, state: AgentState) -> AgentState:
        chain = get_resume_chain()

        result = chain.run(resume_text=state.resume_text)

        raw_skills = result.get("skills", [])

        # ✅ CLEAN SKILLS (VERY IMPORTANT)
        cleaned_skills = [
            skill.replace("-", "").strip().lower()
            for skill in raw_skills
            if skill.strip()
        ]

        state.extracted_skills = cleaned_skills

        self.log(state, f"Extracted skills: {state.extracted_skills}")

        # ✅ SEND MESSAGE
        state.add_message(
            sender=self.name,
            receiver="JobAgent",
            content=f"User skills: {state.extracted_skills}"
        )

        return state