from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.chains.job_chain import get_job_chain

from tools.scoring_tool import score_jobs


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:

        # 🔥 READ MESSAGES
        for msg in state.messages:
            if msg["to"] == "JobAgent":
                self.log(state, f"Received message: {msg['content']}")

        # 1. Fetch jobs
        chain = get_job_chain()
        result = chain.run(skills=state.extracted_skills)

        state.jobs = result.get("jobs", [])

        if len(state.jobs) == 0:
            state.has_jobs = False
            state.needs_strategy = True

            self.log(state, "No jobs found → switching to strategy mode")

            # 🔥 SEND MESSAGE TO STRATEGY AGENT
            state.add_message(
                sender=self.name,
                receiver="StrategyAgent",
                content="No jobs found for current skill set"
            )

            return state

        self.log(state, f"Fetched {len(state.jobs)} jobs")

        # 2. Score jobs
        scored = score_jobs(state.jobs, state.extracted_skills)
        state.match_scores = scored

        # 3. Select top jobs
        state.top_jobs = [item["job"] for item in scored[:5]]

        state.has_jobs = True

        self.log(state, f"Top {len(state.top_jobs)} jobs selected")

        # 🔥 SEND MESSAGE TO ADVISOR AGENT
        state.add_message(
            sender=self.name,
            receiver="AdvisorAgent",
            content=f"Top jobs ready: {len(state.top_jobs)}"
        )

        return state