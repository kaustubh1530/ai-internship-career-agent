import fitz  # PyMuPDF
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# EXTRACT TEXT FROM PDF
# =========================
def extract_text_from_pdf(uploaded_file):
    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


# =========================
# EXTRACT SKILLS USING AI
# =========================
def extract_skills_from_text(text):

    prompt = f"""
    Extract technical skills from the following resume.

    Only return a comma-separated list of skills.
    Do NOT include explanations.

    Resume:
    {text[:3000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    skills_text = response.choices[0].message.content

    skills = [s.strip().lower() for s in skills_text.split(",")]

    return skills

def ai_match_skills(user_skills, job_text):

    prompt = f"""
    You are an AI career assistant.

    Given:
    User Skills: {", ".join(user_skills)}

    Job Description:
    {job_text[:1500]}

    Task:
    1. Identify which user skills are relevant to this job
    2. Return ONLY matched skills as comma-separated list
    3. If none match, return: NONE

    No explanation.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content.strip().lower()

    if result == "none":
        return []

    return [s.strip() for s in result.split(",") if s.strip()]