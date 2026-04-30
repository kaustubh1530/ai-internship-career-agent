from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.job_data_source import load_jobs
from backend.embedding_utils import get_embedding, cosine_similarity


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def run(self, state: AgentState) -> AgentState:

        all_jobs = load_jobs()
        self.log(state, f"Loaded {len(all_jobs)} jobs from data source")

        user_skills = state.extracted_skills or []

        # 🔥 CREATE RESUME EMBEDDING
        resume_text = " ".join(user_skills)
        resume_embedding = get_embedding(resume_text)

        matched_jobs = []

        for job in all_jobs:

            job_text = (
                job.get("title", "") + " " +
                job.get("description", "")
            )

            # 🔥 JOB EMBEDDING
            job_embedding = get_embedding(job_text)

            # 🔥 SEMANTIC SCORE
            semantic_score = cosine_similarity(
                resume_embedding,
                job_embedding
            )

            # 🔥 SKILL SCORE (OLD LOGIC)
            job_text_lower = job_text.lower()

            skill_score = sum(
                1 for skill in user_skills
                if skill in job_text_lower
            )

            # 🔥 FINAL SCORE (HYBRID)
            final_score = (semantic_score * 0.7) + (skill_score * 0.3)

            job["semantic_score"] = float(semantic_score)
            job["skill_score"] = skill_score
            job["score"] = float(final_score)

            self.log(
                state,
                f"{job.get('title')} → semantic: {semantic_score:.2f}, skill: {skill_score}, final: {final_score:.2f}"
            )

            matched_jobs.append(job)

        # 🔥 SORT BY FINAL SCORE
        matched_jobs = sorted(
            matched_jobs,
            key=lambda x: x["score"],
            reverse=True
        )

        state.top_jobs = matched_jobs[:5]

        self.log(state, f"Top {len(state.top_jobs)} jobs selected")

        if state.top_jobs:
            state.add_message(
                sender="JobAgent",
                receiver="AdvisorAgent",
                content=f"Top jobs ready: {len(state.top_jobs)}"
            )

        return state