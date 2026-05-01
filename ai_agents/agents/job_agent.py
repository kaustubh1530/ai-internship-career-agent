from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.embedding_utils import get_embedding, cosine_similarity
import json


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def load_embedded_jobs(self):
        with open("backend/job_embeddings.json", "r") as f:
            return json.load(f)

    def run(self, state: AgentState) -> AgentState:

        # 🔥 LOAD PRECOMPUTED EMBEDDINGS
        all_jobs = self.load_embedded_jobs()
        self.log(state, f"Loaded {len(all_jobs)} precomputed jobs")

        user_skills = state.extracted_skills or []

        # 🔥 RESUME EMBEDDING (ONLY ONCE)
        resume_text = " ".join(user_skills)
        resume_embedding = get_embedding(resume_text)

        matched_jobs = []

        for job in all_jobs:

            job_embedding = job.get("embedding")

            # 🔥 FAST SIMILARITY (NO API CALL)
            semantic_score = cosine_similarity(
                resume_embedding,
                job_embedding
            )

            job_text = (
                job.get("title", "") + " " +
                job.get("description", "")
            ).lower()

            skill_score = sum(
                1 for skill in user_skills
                if skill in job_text
            )

            final_score = (semantic_score * 0.7) + (skill_score * 0.3)

            job["score"] = float(final_score)

            self.log(
                state,
                f"{job.get('title')} → final score: {final_score:.2f}"
            )

            matched_jobs.append(job)

        # 🔥 SORT
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