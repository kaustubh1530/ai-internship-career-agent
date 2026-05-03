from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.job_data_source import load_jobs


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:

        all_jobs = load_jobs()

        self.log(state, f"Loaded {len(all_jobs)} jobs")

        matched_jobs = []

        user_skills = [s.lower() for s in (state.extracted_skills or [])]

        role_filter = (state.role_filter or "").lower()
        location_filter = (state.location_filter or "").lower()

        for job in all_jobs:

            title = job.get("title", "").lower()
            location = job.get("location", "").lower()

            # SAFE FILTERING (FIXED)
            if role_filter and role_filter not in title:
                continue

            if location_filter and location_filter not in location:
                continue

            # SKILL EXTRACTION FIX
            job_text = (
                job.get("title", "") + " " +
                job.get("description", "")
            ).lower()

            # simple keyword match fallback
            skill_score = sum(1 for skill in user_skills if skill in job_text)

            job["score"] = skill_score

            matched_jobs.append(job)

        # IMPORTANT FIX: ALWAYS SHOW TOP JOBS
        matched_jobs = sorted(
            matched_jobs,
            key=lambda x: x["score"],
            reverse=True
        )

        state.top_jobs = matched_jobs[: state.top_n]

        self.log(state, f"Top {len(state.top_jobs)} jobs selected")

        # ALWAYS SEND MESSAGE (FIX)
        state.add_message(
            sender=self.name,
            receiver="AdvisorAgent",
            content=f"Top jobs ready: {len(state.top_jobs)}"
        )

        return state