from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.job_chain import get_job_chain


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:
        chain = get_job_chain()
        result = chain.run(skills=state.extracted_skills)

        state.jobs = result.get("jobs", [])

        if len(state.jobs) > 0:
            state.has_jobs = True
            self.log(state, f"Found {len(state.jobs)} jobs")
        else:
            state.has_jobs = False
            state.needs_strategy = True
            self.log(state, "No jobs found → switching to strategy mode")

        return state