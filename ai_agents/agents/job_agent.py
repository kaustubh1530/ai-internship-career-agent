from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.embedding_utils import get_embedding, cosine_similarity
from backend.memory_utils import get_recent_memory
import json


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def load_embedded_jobs(self):
        with open("backend/job_embeddings.json", "r") as f:
            return json.load(f)

    def run(self, state: AgentState) -> AgentState:

        # LOAD JOBS
        all_jobs = self.load_embedded_jobs()
        self.log(state, f"Loaded {len(all_jobs)} precomputed jobs")

        # LOAD MEMORY
        memory = get_recent_memory()
        self.log(state, f"Loaded memory entries: {len(memory)}")

        user_skills = state.extracted_skills or []

        # RESUME EMBEDDING
        resume_text = " ".join(user_skills)
        resume_embedding = get_embedding(resume_text)

        matched_jobs = []

        # SCORING LOOP
        for job in all_jobs:

            job_embedding = job.get("embedding")

            # Semantic similarity
            semantic_score = cosine_similarity(
                resume_embedding,
                job_embedding
            )

            # Skill matching
            job_text = (
                job.get("title", "") + " " +
                job.get("description", "")
            ).lower()

            skill_score = sum(
                1 for skill in user_skills
                if skill in job_text
            )

            # MEMORY BOOST
            memory_boost = 0
            for past in memory:
                if job.get("title") in past.get("top_jobs", []):
                    memory_boost += 0.1

            # FINAL SCORE
            final_score = (
                (semantic_score * 0.7) +
                (skill_score * 0.3) +
                memory_boost
            )

            job["score"] = float(final_score)

            self.log(
                state,
                f"{job.get('title')} → score: {final_score:.2f}"
            )

            matched_jobs.append(job)

        # SORT + SELECT
        matched_jobs = sorted(
            matched_jobs,
            key=lambda x: x["score"],
            reverse=True
        )

        state.top_jobs = matched_jobs[:5]

        self.log(state, f"Top {len(state.top_jobs)} jobs selected")

        # MESSAGE → ADVISOR
        if state.top_jobs:
            state.add_message(
                sender="JobAgent",
                receiver="AdvisorAgent",
                content=f"Top jobs ready: {len(state.top_jobs)}"
            )

        return state