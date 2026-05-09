def score_jobs(jobs, skills):
    """
    Advanced scoring system:
    - weighted scoring
    - partial semantic matching
    - explainable output
    """

    # SKILL WEIGHTS 
    skill_weights = {
        "python": 3,
        "fastapi": 2,
        "ai": 3,
        "machine learning": 3,
        "sql": 2,
        "communication": 1,
        "rag": 3,
        "faiss": 2, 
        "LangChain": 3, 
        "Vector": 2,
        "Embeddings": 2
    }

    scored_jobs = []

    for job in jobs:
        description = job.get("description", "").lower()

        score = 0
        matched_skills = []
        missing_skills = []

        for skill in skills:
            skill_lower = skill.lower()

            # direct match
            if skill_lower in description:
                weight = skill_weights.get(skill_lower, 1)
                score += weight
                matched_skills.append(skill)
            else:
                # simple semantic fallback (basic)
                if any(keyword in description for keyword in skill_lower.split()):
                    score += 0.5
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)

        scored_jobs.append({
            "job": job,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # sort descending
    scored_jobs.sort(key=lambda x: x["score"], reverse=True)

    return scored_jobs