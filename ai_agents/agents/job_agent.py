import json
import os
import re

from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from backend.job_data_source import load_jobs
from backend.embedding_utils import get_embedding, cosine_similarity


EMBEDDINGS_FILE = "backend/job_embeddings.json"


class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("JobAgent")

    def load_jobs_with_embeddings(self):
        """
        Load precomputed job embeddings if available.
        If embeddings file does not exist, fall back to raw job data.
        """
        if os.path.exists(EMBEDDINGS_FILE):
            with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        return load_jobs()

    def build_job_text(self, job):
        """
        Build searchable text from a job object.
        """
        title = job.get("title", "")
        company = job.get("company", "")
        location = job.get("location", "")
        description = job.get("description", "")

        return f"{title}\n{company}\n{location}\n{description}"

    def build_resume_query(self, state: AgentState):
        """
        Build a semantic search query using resume, extracted skills, and filters.
        """
        skills_text = ", ".join(state.extracted_skills or [])
        role_text = state.role_filter or ""
        resume_text = state.resume_text or ""

        return f"""
Target Role:
{role_text}

Extracted Skills:
{skills_text}

Resume:
{resume_text[:2500]}
"""

    def calculate_skill_score(self, user_skills, job_text):
        """
        Count exact skill matches inside job text.
        """
        if not user_skills:
            return 0, []

        job_text = job_text.lower()

        matched_skills = [
            skill for skill in user_skills
            if skill.lower() in job_text
        ]

        return len(matched_skills), matched_skills

    def calculate_filter_boost(self, job, role_filter, location_filter):
        """
        Soft preference boost. Does not remove jobs.
        """
        boost = 0

        title = job.get("title", "").lower()
        location = job.get("location", "").lower()
        description = job.get("description", "").lower()

        job_text = f"{title} {location} {description}"

        if role_filter and role_filter in job_text:
            boost += 5

        if location_filter and location_filter in location:
            boost += 5

        return boost

    def normalize_text(self, text):
        """
        Normalize text for duplicate detection.
        """
        text = (text or "").lower().strip()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def deduplicate_jobs(self, scored_jobs):
        """
        Remove repeated jobs that have the same title and company.
        Keeps the highest-scoring version.
        """
        unique_jobs = {}
        fallback_jobs = []

        for job in scored_jobs:
            title = self.normalize_text(job.get("title", ""))
            company = self.normalize_text(job.get("company", ""))

            duplicate_key = f"{title}|{company}"

            if duplicate_key not in unique_jobs:
                unique_jobs[duplicate_key] = job
            else:
                fallback_jobs.append(job)

        return list(unique_jobs.values()), fallback_jobs

    def run(self, state: AgentState) -> AgentState:
        all_jobs = self.load_jobs_with_embeddings()

        self.log(state, f"Loaded {len(all_jobs)} jobs for semantic matching")

        if not all_jobs:
            state.top_jobs = []
            state.has_jobs = False
            state.needs_strategy = True
            self.log(state, "No jobs found in data source")
            return state

        user_skills = [
            skill.lower().strip()
            for skill in (state.extracted_skills or [])
            if skill.strip()
        ]

        role_filter = (state.role_filter or "").lower().strip()
        location_filter = (state.location_filter or "").lower().strip()

        resume_query = self.build_resume_query(state)
        resume_embedding = get_embedding(resume_query)

        scored_jobs = []

        for job in all_jobs:
            job_text = self.build_job_text(job)
            job_embedding = job.get("embedding")

            if not job_embedding:
                job_embedding = get_embedding(job_text)

            semantic_score = cosine_similarity(resume_embedding, job_embedding)

            skill_score, matched_skills = self.calculate_skill_score(
                user_skills=user_skills,
                job_text=job_text
            )

            filter_boost = self.calculate_filter_boost(
                job=job,
                role_filter=role_filter,
                location_filter=location_filter
            )

            semantic_points = semantic_score * 100

            final_score = (
                semantic_points * 0.80
                + skill_score * 3
                + filter_boost
            )

            job["semantic_score"] = round(float(semantic_score), 3)
            job["skill_score"] = skill_score
            job["matched_skills"] = matched_skills
            job["score"] = round(float(final_score), 2)

            scored_jobs.append(job)

        scored_jobs = sorted(
            scored_jobs,
            key=lambda job: job.get("score", 0),
            reverse=True
        )

        unique_jobs, fallback_duplicates = self.deduplicate_jobs(scored_jobs)

        requested_top_n = state.top_n or 5
        minimum_jobs = 3
        target_count = max(minimum_jobs, requested_top_n)

        selected_jobs = unique_jobs[:target_count]

        # If there are not enough unique jobs, fill with fallback duplicates.
        if len(selected_jobs) < target_count:
            needed = target_count - len(selected_jobs)
            selected_jobs.extend(fallback_duplicates[:needed])

        state.top_jobs = selected_jobs

        state.has_jobs = len(state.top_jobs) > 0
        state.needs_strategy = not state.has_jobs

        self.log(
            state,
            f"Returning {len(state.top_jobs)} diversified semantic job matches"
        )

        for job in state.top_jobs:
            self.log(
                state,
                f"Selected: {job.get('title')} at {job.get('company')} | score={job.get('score')}"
            )

        state.add_message(
            sender=self.name,
            receiver="AdvisorAgent",
            content=f"Diversified semantic job matches ready: {len(state.top_jobs)}"
        )

        return state