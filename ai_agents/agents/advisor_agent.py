from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.advisor_chain import get_advisor_chain
from backend.memory_utils import get_recent_memory


class AdvisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("AdvisorAgent")

    def run(self, state: AgentState) -> AgentState:

        # READ MESSAGES
        for msg in state.messages:
            if msg.get("to") == self.name:
                self.log(state, f"Received message: {msg.get('content')}")

        # SAFETY CHECK
        if not state.top_jobs:
            self.log(state, "No top jobs available → skipping AdvisorAgent")
            return state

        # LOAD MEMORY
        memory = get_recent_memory()
        self.log(state, f"Using memory entries: {len(memory)}")

        # RUN CHAIN
        chain = get_advisor_chain()

        result = chain.run(
            resume=state.resume_text,
            jobs=state.top_jobs,
            skills=state.extracted_skills,
            history=memory   # 🔥 NEW
        )

        # STORE OUTPUT
        state.recommendations = result.get("recommendations", [])
        state.final_answer = result.get("summary", "")

        # LOG
        self.log(
            state,
            f"Generated recommendations using top {len(state.top_jobs)} jobs"
        )

        return state