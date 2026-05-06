from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.job_data_source import load_jobs


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:

        all_jobs = load_jobs()
        self.log(state, f"Loaded {len(all_jobs)} jobs")

        user_skills = [s.lower() for s in (state.extracted_skills or [])]

        role_filter = (state.role_filter or "").lower()
        location_filter = (state.location_filter or "").lower()

        scored_jobs = []

        for job in all_jobs:
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()
            location = job.get("location", "").lower()

            # -------------------------
            # SOFT FILTERING (IMPORTANT FIX)
            # -------------------------
            role_match = role_filter in title if role_filter else True
            location_match = location_filter in location if location_filter else True

            filter_score = 1 if (role_match and location_match) else 0

            # -------------------------
            # KEYWORD MATCHING (MAIN FIX)
            # -------------------------
            job_text = title + " " + description

            skill_score = sum(
                1 for skill in user_skills
                if skill in job_text
            )

            # -------------------------
            # FINAL SCORE
            # -------------------------
            final_score = (skill_score * 2) + filter_score

            job["score"] = final_score

            scored_jobs.append(job)

        # -------------------------
        # SORT ALL JOBS (IMPORTANT)
        # -------------------------
        scored_jobs = sorted(
            scored_jobs,
            key=lambda x: x["score"],
            reverse=True
        )

        # GUARANTEED JOB OUTPUT
        top_n = state.top_n or 5

        # ALWAYS RETURN AT LEAST 3 JOBS
        min_jobs = max(3, top_n)

        state.top_jobs = scored_jobs[:min_jobs]

        self.log(state, f"Returning {len(state.top_jobs)} jobs (guaranteed)")

        # SEND MESSAGE
        state.add_message(
            sender=self.name,
            receiver="AdvisorAgent",
            content=f"Top jobs ready: {len(state.top_jobs)}"
        )

        return state