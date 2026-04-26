from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.advisor_chain import get_advisor_chain


class AdvisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("AdvisorAgent")

    def run(self, state: AgentState) -> AgentState:
        """
        Generates career recommendations based on:
        - User resume
        - Top matched jobs (after scoring)
        """

        # -------------------------
        # SAFETY CHECK
        # -------------------------
        if not state.top_jobs:
            self.log(state, "No top jobs available → skipping AdvisorAgent")
            return state

        # -------------------------
        # RUN LLM CHAIN
        # -------------------------
        chain = get_advisor_chain()

        result = chain.run(
            resume=state.resume_text,
            jobs=state.top_jobs,
            skills=state.extracted_skills
        )
        # -------------------------
        # STORE OUTPUT
        # -------------------------
        state.recommendations = result.get("recommendations", [])
        state.final_answer = result.get("summary", "")

        # -------------------------
        # LOGGING
        # -------------------------
        self.log(
            state,
            f"Generated recommendations using top {len(state.top_jobs)} jobs"
        )

        return state
