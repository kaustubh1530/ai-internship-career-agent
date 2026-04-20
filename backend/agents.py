from ai_langchain.chains.resume_chain import get_resume_chain
from ai_langchain.chains.job_chain import get_job_chain
from ai_langchain.chains.advisor_chain import get_advisor_chain


def resume_agent(user_skills):
    chain = get_resume_chain()

    skills_text = ", ".join(user_skills)

    result = chain.run(user_skills=skills_text)

    return result


def job_agent(job_text):
    chain = get_job_chain()

    return chain.invoke({
        "job_text": job_text[:1500]
    })


def advisor_agent(user_skills, job_text):
    chain = get_advisor_chain()

    return chain.invoke({
        "user_skills": ", ".join(user_skills),
        "job_text": job_text[:1500]
    })
