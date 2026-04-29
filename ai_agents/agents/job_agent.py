from ai_agents.base import BaseAgent
from ai_agents.state import AgentState

from backend.search_jobs import search_jobs  # ✅ REAL JOB SYSTEM
from tools.scoring_tool import score_jobs


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:

        # -------------------------
        # READ MESSAGES
        # -------------------------
        for msg in state.messages:
            if msg["to"] == "JobAgent":
                self.log(state, f"Received message: {msg['content']}")

        # -------------------------
        # BUILD QUERY FROM SKILLS
        # -------------------------
        if not state.extracted_skills:
            query = "software engineer"
        else:
            query = " ".join(state.extracted_skills[:5])

        self.log(state, f"Searching jobs for: {query}")

        # -------------------------
        # 🔥 REAL JOB SEARCH
        # -------------------------
        jobs = search_jobs(query, top_k=10)

        if not jobs:
            state.has_jobs = False
            state.needs_strategy = True

            self.log(state, "No jobs found → switching to strategy mode")

            state.add_message(
                sender=self.name,
                receiver="StrategyAgent",
                content="No jobs found for current skill set"
            )

            return state

        self.log(state, f"Fetched {len(jobs)} real jobs")

        # -------------------------
        # SCORE JOBS
        # -------------------------
        scored = score_jobs(jobs, state.extracted_skills)
        state.match_scores = scored

        # -------------------------
        # SELECT TOP JOBS
        # -------------------------
        state.top_jobs = [item["job"] for item in scored[:5]]

        state.has_jobs = True

        self.log(state, f"Top {len(state.top_jobs)} jobs selected")

        # -------------------------
        # SEND MESSAGE
        # -------------------------
        state.add_message(
            sender=self.name,
            receiver="AdvisorAgent",
            content=f"Top jobs ready: {len(state.top_jobs)}"
        )

        return state