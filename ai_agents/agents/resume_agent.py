from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.resume_chain import get_resume_chain


class ResumeAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResumeAgent")

    def run(self, state: AgentState) -> AgentState:
        chain = get_resume_chain()

        result = chain.run(resume_text=state.resume_text)

        state.extracted_skills = result.get("skills", [])

        self.log(state, f"Extracted skills: {state.extracted_skills}")

        # 🔥 SEND MESSAGE TO JOB AGENT
        state.add_message(
            sender=self.name,
            receiver="JobAgent",
            content=f"User skills: {state.extracted_skills}"
        )

        return state