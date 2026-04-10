from tools.job_tools import search_jobs, extract_skills_from_description


def handle_user_query(user_query, user_skills):
    print("\n[Agent Thought] Looking for roles that fit your background...\n")

    jobs = search_jobs(user_query)

    if not jobs:
        print("No jobs found.")
        return

    user_skills_lower = [u.lower() for u in user_skills]

    valid_jobs = []

    for job in jobs:
        description = job.get("description") or ""

        skills = extract_skills_from_description(description)

        if not skills:
            skills = []

        matched = [s for s in skills if s in user_skills_lower]
        missing = [s for s in skills if s not in user_skills_lower]

        if len(skills) == 0:
            score = 0
        else:
            score = int((len(matched) / len(skills)) * 100)

        valid_jobs.append((job, score, matched, missing))

    valid_jobs.sort(key=lambda x: x[1], reverse=True)

    if not valid_jobs:
        print("No strong matches found.")
        return

    print("\n[Agent Observation] Top matching jobs:\n")

    for job, score, matched, missing in valid_jobs[:5]:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Match Score: {score}%")
        print(f"Matched Skills: {matched if matched else 'None'}")
        print(f"Missing Skills: {missing if missing else 'None'}")
        print(f"Apply Here: {job['url']}")
        print("-" * 60)

    print("\n[Final Answer]")
    print("These jobs are ranked based on real skill matching using AI.")
