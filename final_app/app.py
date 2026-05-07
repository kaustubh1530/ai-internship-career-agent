import streamlit as st
import sys
import os
import re

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_agent import run_multi_agent_system
from backend.resume_parser import extract_text_from_pdf

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Career Intelligence System",
    page_icon="🚀",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    color: #9ca3af;
    font-size: 18px;
    margin-bottom: 25px;
}

.metric-card {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

.skill-pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background-color: #064e3b;
    color: #d1fae5;
    font-size: 13px;
    margin-right: 6px;
    margin-top: 6px;
}

.advice-card {
    background-color: #111827;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #1f2937;
    color: white;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# HELPERS
# ==============================
def format_links(text):
    if not text:
        return "No career recommendation generated."

    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        r'<a href="\2" target="_blank">\1</a>',
        text
    )

    return text.replace("\n", "<br>")


def render_skill_pills(skills):
    if not skills:
        st.caption("No exact skills matched. Ranked mainly by semantic similarity.")
        return

    pills_html = ""
    for skill in skills[:8]:
        pills_html += f"<span class='skill-pill'>{skill}</span>"

    st.markdown(pills_html, unsafe_allow_html=True)


def render_job_card(job, index):
    title = job.get("title", "Untitled Role")
    company = job.get("company", "Unknown Company")
    location = job.get("location", "Unknown Location")
    url = job.get("url", "#")

    match_percentage = int(job.get("match_percentage", 0))
    match_level = job.get("match_level", "Match")
    semantic_score = job.get("semantic_score", 0)
    skill_score = job.get("skill_score", 0)
    matched_skills = job.get("matched_skills", [])
    reason = job.get(
        "match_reason",
        "This role was selected based on resume relevance."
    )

    with st.container(border=True):
        top_col, score_col = st.columns([4, 1])

        with top_col:
            st.subheader(f"{index}. {title}")
            st.markdown(f"**{company}** — {location}")

        with score_col:
            st.metric("Match", f"{match_percentage}%")

        st.progress(min(match_percentage / 100, 1.0))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**Match Level:** {match_level}")

        with col2:
            st.markdown(f"**AI Similarity:** {semantic_score}")

        with col3:
            st.markdown(f"**Skill Matches:** {skill_score}")

        st.markdown("**Matched Skills:**")
        render_skill_pills(matched_skills)

        st.markdown("**Why this matched:**")
        st.info(reason)

        if url and url != "#":
            st.link_button("Apply Now", url, use_container_width=True)
        else:
            st.warning("No application link available.")


# ==============================
# HEADER
# ==============================
st.markdown(
    '<div class="main-title">🚀 AI Career Intelligence System</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Multi-Agent AI system for resume analysis, semantic job matching, and career strategy.</div>',
    unsafe_allow_html=True
)

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("👤 Resume")
uploaded_file = st.sidebar.file_uploader("Upload Resume PDF", type=["pdf"])

st.sidebar.markdown("### 🔍 Job Preferences")
role = st.sidebar.text_input(
    "Target Role",
    placeholder="Example: Software Engineer Intern"
)
location = st.sidebar.text_input(
    "Preferred Location",
    placeholder="Example: Remote, Maryland"
)
top_n = st.sidebar.slider("Number of Jobs", 3, 10, 3)

resume_text = None

if uploaded_file:
    with st.sidebar.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.sidebar.success("Resume loaded successfully")

# ==============================
# MAIN
# ==============================
st.markdown("## 🧠 AI Career Analysis")

if resume_text:
    if st.button("🚀 Run AI Analysis", use_container_width=True):

        with st.spinner("Running multi-agent AI system..."):
            result = run_multi_agent_system(
                resume_text,
                role=role,
                location=location,
                top_n=top_n
            )

        # --------------------------
        # JOB MATCHES
        # --------------------------
        st.markdown("## 💼 Top Job Matches")

        if result.top_jobs:
            for index, job in enumerate(result.top_jobs, start=1):
                render_job_card(job, index)
        else:
            st.error("No jobs found. Try removing filters or refreshing job data.")

        # --------------------------
        # CAREER RECOMMENDATIONS
        # --------------------------
        st.markdown("## 🎯 Career Recommendations")

        formatted_advice = format_links(result.final_answer)
        st.markdown(
            f'<div class="advice-card">{formatted_advice}</div>',
            unsafe_allow_html=True
        )

        # --------------------------
        # LOGS
        # --------------------------
        with st.expander("🧠 View AI System Logs"):
            for log in result.logs:
                st.write(log)

else:
    st.warning("Please upload your resume to start.")

st.markdown("---")
st.caption("🚀 Built by Kaustubh Patil | Multi-Agent AI Career Intelligence System")