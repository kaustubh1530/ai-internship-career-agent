# Global shared context (simple version)

user_context = {
    "skills": None,
    "jobs": None
}

def set_user_skills(skills):
    user_context["skills"] = skills

def get_user_skills():
    return user_context["skills"]


def set_jobs(jobs):
    user_context["jobs"] = jobs

def get_jobs():
    return user_context["jobs"]