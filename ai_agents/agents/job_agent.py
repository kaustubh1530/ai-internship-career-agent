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

        # Skill aliases make matching more realistic.
        # This fixes the issue where semantic match is good but exact skill match is 0.
        self.skill_aliases = {
            "python": ["python", "backend", "api", "scripting"],
            "java": ["java", "object oriented", "oop"],
            "javascript": ["javascript", "js", "frontend", "web development"],
            "html": ["html", "web page", "frontend"],
            "css": ["css", "styling", "frontend"],
            "fastapi": ["fastapi", "api", "rest api", "backend"],
            "flask": ["flask", "api", "backend"],
            "restful apis": ["rest", "restful", "api", "apis", "endpoint"],
            "rest api development": ["rest", "api", "apis", "endpoint"],
            "sql": ["sql", "database", "postgresql", "sqlite"],
            "sqlite": ["sqlite", "sql", "database"],
            "postgresql": ["postgresql", "postgres", "sql", "database"],
            "git": ["git", "github", "version control"],
            "github": ["github", "git", "version control"],
            "unit testing": ["testing", "unit testing", "test cases", "qa", "quality assurance"],
            "code quality": ["code quality", "testing", "qa", "debugging"],
            "system integration": ["integration", "systems", "software systems"],
            "fullstack development": ["full stack", "fullstack", "frontend", "backend", "web application"],
            "full-stack development": ["full stack", "fullstack", "frontend", "backend", "web application"],
            "ai": ["ai", "artificial intelligence", "machine learning", "ml"],
            "openai apis": ["openai", "ai", "llm", "api"],
            "rag": ["rag", "retrieval augmented generation", "vector search", "semantic search"],
            "faiss": ["faiss", "vector database", "vector search", "similarity search"],
            "langchain": ["langchain", "llm", "ai pipeline", "agent"],
            "vector embeddings": ["embedding", "embeddings", "vector", "semantic search"],
            "semantic search": ["semantic", "search", "vector search", "similarity search"],
            "streamlit": ["streamlit", "dashboard", "web app", "ui"],
            "pydantic": ["pydantic", "validation", "data validation"],
            "json": ["json", "data", "api response"],
            "agile methodologies": ["agile", "scrum", "team collaboration"],
            "data extraction and validation": ["data extraction", "validation", "parsing"],
            "prompt engineering": ["prompt", "llm", "ai"],
            "ats optimization": ["ats", "resume", "career"],
        }

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

    def normalize_text(self, text):
        """
        Normalize text for matching and deduplication.
        """
        text = (text or "").lower().strip()
        text = re.sub(r"[^a-z0-9\s\+\#\.]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def get_aliases_for_skill(self, skill):
        """
        Return aliases for a skill.
        If no aliases exist, return the skill itself.
        """
        normalized_skill = self.normalize_text(skill)

        aliases = self.skill_aliases.get(normalized_skill, [normalized_skill])

        return [self.normalize_text(alias) for alias in aliases]

    def calculate_skill_score(self, user_skills, job_text):
        """
        Smarter skill matching:
        - exact skill match
        - alias match
        - related term match
        """
        if not user_skills:
            return 0, []

        normalized_job_text = self.normalize_text(job_text)

        matched_skills = []

        for skill in user_skills:
            normalized_skill = self.normalize_text(skill)
            aliases = self.get_aliases_for_skill(normalized_skill)

            for alias in aliases:
                if alias and alias in normalized_job_text:
                    matched_skills.append(skill)
                    break

        # Remove duplicates while preserving order
        unique_matched_skills = []
        seen = set()

        for skill in matched_skills:
            clean_skill = skill.strip().lower()
            if clean_skill not in seen:
                unique_matched_skills.append(skill)
                seen.add(clean_skill)

        return len(unique_matched_skills), unique_matched_skills

    def calculate_filter_boost(self, job, role_filter, location_filter):
        """
        Soft preference boost. Does not remove jobs.
        """
        boost = 0

        title = self.normalize_text(job.get("title", ""))
        location = self.normalize_text(job.get("location", ""))
        description = self.normalize_text(job.get("description", ""))

        job_text = f"{title} {location} {description}"

        role_filter = self.normalize_text(role_filter)
        location_filter = self.normalize_text(location_filter)

        if role_filter and role_filter in job_text:
            boost += 5

        if location_filter and location_filter in location:
            boost += 5

        return boost

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

    def get_match_level(self, percentage):
        """
        Convert percentage into a human-readable match level.
        """
        if percentage >= 80:
            return "Strong Match"
        if percentage >= 60:
            return "Good Match"
        if percentage >= 40:
            return "Moderate Match"
        return "Learning Match"

    def build_match_reason(self, matched_skills, semantic_score):
        """
        Build a short explanation for why the job matched.
        """
        if matched_skills:
            skills_preview = ", ".join(matched_skills[:5])
            return f"Matched based on skills such as {skills_preview} and overall resume similarity."

        if semantic_score >= 0.45:
            return "Matched because the job description is semantically related to your software engineering background."

        return "Included as a related opportunity based on software engineering internship relevance."

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
                semantic_points * 0.75
                + skill_score * 4
                + filter_boost
            )

            match_percentage = max(0, min(100, round(final_score)))

            job["semantic_score"] = round(float(semantic_score), 3)
            job["skill_score"] = skill_score
            job["matched_skills"] = matched_skills
            job["score"] = round(float(final_score), 2)
            job["match_percentage"] = match_percentage
            job["match_level"] = self.get_match_level(match_percentage)
            job["match_reason"] = self.build_match_reason(
                matched_skills=matched_skills,
                semantic_score=semantic_score
            )

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

        if len(selected_jobs) < target_count:
            needed = target_count - len(selected_jobs)
            selected_jobs.extend(fallback_duplicates[:needed])

        state.top_jobs = selected_jobs
        state.has_jobs = len(state.top_jobs) > 0
        state.needs_strategy = not state.has_jobs

        self.log(
            state,
            f"Returning {len(state.top_jobs)} explainable semantic job matches"
        )

        for job in state.top_jobs:
            self.log(
                state,
                f"Selected: {job.get('title')} at {job.get('company')} | match={job.get('match_percentage')}% | skills={job.get('matched_skills')}"
            )

        state.add_message(
            sender=self.name,
            receiver="AdvisorAgent",
            content=f"Explainable semantic job matches ready: {len(state.top_jobs)}"
        )

        return state