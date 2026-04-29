from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.job_data_source import load_jobs


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:

        all_jobs = load_jobs()
        self.log(state, f"Loaded {len(all_jobs)} jobs from data source")

        user_skills = state.extracted_skills or []
        matched_jobs = []

        self.log(state, f"User skills: {user_skills}")

        for job in all_jobs:

            # 🔥 Combine ALL job text
            job_text = (
                job.get("title", "") + " " +
                job.get("description", "")
            ).lower()

            score = 0

            # 🔥 Flexible matching
            for skill in user_skills:
                if skill in job_text:
                    score += 1

            # 🔥 Fallback: if nothing matches, still give base score
            if score == 0:
                if "software" in job_text or "engineer" in job_text:
                    score = 1  # fallback relevance

            job["score"] = score

            self.log(state, f"{job.get('title')} → score: {score}")

            matched_jobs.append(job)

        # 🔥 SORT ALL JOBS (even low score)
        matched_jobs = sorted(
            matched_jobs,
            key=lambda x: x["score"],
            reverse=True
        )

        # 🔥 ALWAYS RETURN TOP JOBS (CRITICAL FIX)
        state.top_jobs = matched_jobs[:5]

        self.log(state, f"Top {len(state.top_jobs)} jobs selected")

        # MESSAGE PASSING
        state.add_message(
            sender="JobAgent",
            receiver="AdvisorAgent",
            content=f"Top jobs ready: {len(state.top_jobs)}"
        )

        return state