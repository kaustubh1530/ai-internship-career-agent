from io import BytesIO
import os

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

from ai_langchain.context import set_user_skills


# ENV + OPENAI CLIENT
load_dotenv()


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing OPENAI_API_KEY. Add it locally in .env or in Railway Variables."
        )

    return OpenAI(api_key=api_key)


# EXTRACT TEXT FROM PDF
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file using pypdf.
    Works locally and on Railway.
    """

    try:
        pdf_bytes = uploaded_file.read()
        pdf_stream = BytesIO(pdf_bytes)

        reader = PdfReader(pdf_stream)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as error:
        return f"Error reading PDF: {error}"


# EXTRACT SKILLS USING AI
def extract_skills_from_text(text):
    """
    Extract technical skills from resume text using OpenAI.
    Returns a clean list of lowercase skills.
    """

    if not text or text.startswith("Error reading PDF"):
        return []

    client = get_openai_client()

    prompt = f"""
Extract technical skills from the following resume.

Only return a comma-separated list of skills.
Do NOT include explanations.

Resume:
{text[:4000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    skills_text = response.choices[0].message.content or ""

    skills = [
        skill.strip().lower()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    set_user_skills(skills)

    return skills


# AI SKILL MATCHING
def ai_match_skills(user_skills, job_text):
    """
    Use AI to identify which user skills match a job description.
    """

    if not user_skills or not job_text:
        return []

    client = get_openai_client()

    prompt = f"""
You are an AI career assistant.

Given:
User Skills: {", ".join(user_skills)}

Job Description:
{job_text[:2000]}

Task:
1. Identify which user skills are relevant to this job
2. Return ONLY matched skills as comma-separated list
3. If none match, return: NONE

No explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip().lower()

    if result == "none":
        return []

    return [
        skill.strip()
        for skill in result.split(",")
        if skill.strip()
    ]