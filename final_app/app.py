import streamlit as st
import sys
import os

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Backend imports
from backend.search_jobs import search
from backend.resume_parser import (
    extract_text_from_pdf,
    extract_skills_from_text,
    ai_match_skills
)
from backend.agents import resume_agent, advisor_agent

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🚀",
    layout="wide"
)

# ==============================
# GLOBAL STYLING
# ==============================
st.markdown("""
<style>
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #222;
}
.title {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.title("🚀 AI Internship Career Agent")
st.markdown("AI-powered job matching using RAG + Resume Intelligence")
st.markdown("---")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("🔍 Search Jobs")

query = st.sidebar.text_input("Job Role", placeholder="Software Engineer Intern")

skills_input = st.sidebar.text_area(
    "Your Skills",
    placeholder="Python, SQL, Machine Learning"
)

uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

search_button = st.sidebar.button("Search Jobs 🚀")

# ==============================
# SKILLS
# ==============================
user_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]

IGNORE_SKILLS = ["vs code", "postman", "jupyter", "git", "github"]

# ==============================
# RESUME PROCESSING
# ==============================
if uploaded_file:
    with st.sidebar.spinner("📄 Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.sidebar.spinner("🧠 Extracting skills..."):
        extracted_skills = extract_skills_from_text(resume_text)

    extracted_skills = [s for s in extracted_skills if s not in IGNORE_SKILLS]
    user_skills = extracted_skills[:10]

    st.sidebar.success("✅ Skills extracted")
    st.sidebar.write(", ".join(user_skills))

# ==============================
# PROFILE SECTION
# ==============================
st.markdown("## 👤 Your Profile")

colA, colB = st.columns(2)

with colA:
    st.markdown("### 🧠 Skills")
    if user_skills:
        st.success(", ".join(user_skills))
    else:
        st.warning("No skills provided")

with colB:
    st.markdown("### 📊 Search Info")
    st.write(f"**Role:** {query if query else 'Not set'}")

# ==============================
# MAIN LOGIC
# ==============================
if search_button:

    if not query:
        st.warning("⚠️ Enter a job role")
        st.stop()

    with st.spinner("🔎 Searching and analyzing jobs..."):
        jobs = search(query)

    if not jobs:
        st.error("No jobs found")
        st.stop()

    # LIMIT FOR SPEED
    jobs = jobs[:3]

    # RUN RESUME AGENT ONCE (IMPORTANT)
    resume_analysis = resume_agent(user_skills)

    st.success(f"Found {len(jobs)} matches")
    st.markdown("## 🎯 Top Matches")

    # ==============================
    # JOB LOOP
    # ==============================
    for i, job in enumerate(jobs):

        job_text = (
            job.get("title", "") + " " +
            job.get("description", "")
        ).lower()

        # ==============================
        # MATCHING
        # ==============================
        matched = ai_match_skills(user_skills, job_text)

        if len(matched) >= 2:
            missing = [s for s in user_skills if s not in matched][:5]
        else:
            missing = []

        ai_match = False
        if not matched:
            matched = ["Relevant (AI Match)"]
            ai_match = True

        # ==============================
        # ADVISOR (ONLY 1 AI CALL HERE)
        # ==============================
        advice = advisor_agent(user_skills, job_text)

        # ==============================
        # RANK LABEL
        # ==============================
        if i == 0:
            st.markdown("## 🥇 Top Match")
        elif i == 1:
            st.markdown("## 🥈 Strong Match")
        else:
            st.markdown("## 🥉 Other Match")

        # ==============================
        # CARD
        # ==============================
        with st.container():

            st.markdown(f"""
            <div class="card">
                <div class="title">💼 {job.get('title')}</div>
                <p>🏢 {job.get('company')} | 📍 {job.get('location')}</p>
            </div>
            """, unsafe_allow_html=True)

            # SCORE BAR
            score = job.get("score", 0)
            st.progress(min(score, 1.0))
            st.caption(f"⭐ Match Score: {round(score, 2)}")

            # ==============================
            # SKILLS
            # ==============================
            st.markdown("### 🧠 Skill Match")

            col1, col2 = st.columns(2)

            with col1:
                st.success(", ".join(matched))

            with col2:
                if missing:
                    st.warning(", ".join(missing))
                else:
                    st.write("Strong match 🚀")

            # ==============================
            # INSIGHTS
            # ==============================
            st.markdown("### 🤖 AI Insights")

            st.markdown("**Resume Analysis**")
            st.info(resume_analysis)

            st.markdown("**Career Advice**")
            st.success(advice)

            # ==============================
            # WHY MATCH
            # ==============================
            if ai_match:
                st.info("Matched using AI semantic search (RAG)")
            else:
                st.info(f"Matched skills: {', '.join(matched)}")

            # DESCRIPTION
            st.markdown("### 📝 Description")
            st.write(job.get("description", "")[:250] + "...")

            # APPLY
            if job.get("url"):
                st.markdown(f"[👉 Apply Here]({job['url']})")

            st.markdown("---")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built by Kaustubh Patil | AI Career Agent")