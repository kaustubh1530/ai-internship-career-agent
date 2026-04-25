from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.advisor_chain import get_advisor_chain


class AdvisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("AdvisorAgent")

    def run(self, state: AgentState) -> AgentState:
        chain = get_advisor_chain()

        result = chain.run(
            resume=state.resume_text,
            jobs=state.jobs
        )

        state.recommendations = result.get("recommendations", [])
        state.final_answer = result.get("summary", "")

        self.log(state, "Generated job-based recommendations")

        return state