import streamlit as st
import sys
import os

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.search_jobs import search
from backend.resume_parser import (
    extract_text_from_pdf,
    extract_skills_from_text,
    ai_match_skills
)
from backend.agents import resume_agent, job_agent, advisor_agent

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🚀",
    layout="wide"
)

# ==============================
# HEADER
# ==============================
st.title("🚀 AI Internship Career Agent")
st.markdown("AI-powered job matching using RAG + Resume Intelligence")

st.markdown("---")

# ==============================
# SIDEBAR INPUTS
# ==============================
st.sidebar.header("🔍 Search Jobs")

query = st.sidebar.text_input("Job Role", placeholder="Software Engineer Intern")

skills_input = st.sidebar.text_area(
    "Your Skills (optional)",
    placeholder="Python, SQL, Machine Learning"
)

uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

search_button = st.sidebar.button("Search Jobs 🚀")

# ==============================
# SKILL PROCESSING
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
# MAIN LOGIC
# ==============================
if search_button:

    if not query:
        st.warning("⚠️ Please enter a job role")
        st.stop()

    with st.spinner("🚀 Running AI job matching..."):
        jobs = search(query)

    st.success(f"Found {len(jobs)} matches")
    st.markdown("## 🎯 Top Matches For You")

    # limit jobs for performance
    for job in jobs[:3]:

        job_text = (
            job.get("title", "") + " " +
            job.get("description", "")
        ).lower()

        # ==============================
        # AI SKILL MATCH
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
        # AGENTS (CORRECT POSITION)
        # ==============================
        resume_analysis = resume_agent(user_skills)
        job_analysis = job_agent(job_text)
        advice = advisor_agent(user_skills, job_text)

        # ==============================
        # UI CARD
        # ==============================
        with st.container():

            st.markdown("""
                <div style="
                    border:1px solid #ddd;
                    border-radius:10px;
                    padding:15px;
                    margin-bottom:15px;
                    background-color:#fafafa;
                ">
            """, unsafe_allow_html=True)

            st.markdown(f"### 💼 {job.get('title', 'No Title')}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"🏢 **Company:** {job.get('company', 'N/A')}")
                st.write(f"📍 **Location:** {job.get('location', 'N/A')}")

            with col2:
                st.write(f"⭐ **Match Score:** {round(job.get('score', 0), 2)}")

            # ==============================
            # SKILL MATCH
            # ==============================
            st.markdown("#### 🧠 Skill Match")

            col3, col4 = st.columns(2)

            with col3:
                st.success(", ".join(matched))

            with col4:
                if missing:
                    st.warning(", ".join(missing))
                else:
                    st.write("Strong match 🚀")

            # ==============================
            # AGENT INSIGHTS
            # ==============================
            st.markdown("#### 🧠 Resume Insights")
            st.info(resume_analysis)

            st.markdown("#### 📊 Job Insights")
            st.info(job_analysis)

            st.markdown("#### 💡 Career Advice")
            st.success(advice)

            # ==============================
            # WHY MATCH
            # ==============================
            st.markdown("#### 💡 Why this matches you")

            if ai_match:
                st.info("Matched using AI semantic search (RAG).")
            else:
                st.info(f"Matched skills: {', '.join(matched)}")

            # DESCRIPTION
            st.markdown("#### 📝 Description")
            st.write(job.get("description", "")[:250] + "...")

            if job.get("url"):
                st.markdown(f"[👉 Apply Here]({job['url']})")

            st.markdown("</div>", unsafe_allow_html=True)