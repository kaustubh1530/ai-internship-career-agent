import streamlit as st
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_agent import run_multi_agent_system
from backend.resume_parser import extract_text_from_pdf

st.set_page_config(
    page_title="AI Career Intelligence System",
    page_icon="🚀",
    layout="wide"
)

# STYLE
st.markdown("""
<style>
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #222;
    color: white;
}
.card a {
    color: #4da3ff;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# HELPERS
def format_links(text):
    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        r'<a href="\2" target="_blank">\1</a>',
        text
    )
    return text.replace("\n", "<br>")

def job_card(job):
    return f"""
    <div class="card">
        <h4>{job.get("title")}</h4>
        <p>{job.get("company")} — {job.get("location")}</p>
        <a href="{job.get("url")}" target="_blank">Apply Here</a>
    </div>
    """

# HEADER
st.title("🚀 AI Career Intelligence System")
st.markdown("---")

# SIDEBAR
st.sidebar.header("👤 Upload Resume")

uploaded_file = st.sidebar.file_uploader("Upload Resume", type=["pdf"])

# 🔥 NEW FILTERS
st.sidebar.markdown("### 🔍 Job Preferences")

role = st.sidebar.text_input("Job Role (optional)")
location = st.sidebar.text_input("Location (optional)")
top_n = st.sidebar.slider("Number of Jobs", 1, 10, 5)

resume_text = None

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.sidebar.success("Resume loaded")

# MAIN
st.markdown("## 🧠 AI Career Analysis")

if resume_text:
    if st.button("🚀 Run AI Analysis"):

        result = run_multi_agent_system(
            resume_text,
            role=role,
            location=location,
            top_n=top_n
        )

        # JOBS DISPLAY
        st.markdown("## 💼 Top Job Matches")

        if result.top_jobs:

            for job in result.top_jobs:
                st.markdown(f"""
                <div class="card">
                    <h4>{job.get("title")}</h4>
                    <p><b>{job.get("company")}</b> — {job.get("location")}</p>
                    <p>Match Score: {job.get("score")}</p>
                    <a href="{job.get("url")}" target="_blank">Apply Here</a>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("Something went wrong — no jobs found")
        # AI OUTPUT
        st.markdown("## 🎯 Career Recommendations")

        formatted = format_links(result.final_answer or "")
        st.markdown(f'<div class="card">{formatted}</div>', unsafe_allow_html=True)

        # LOGS
        with st.expander("🧠 View AI Logs"):
            for log in result.logs:
                st.write(log)

else:
    st.warning("Upload resume to start")

st.markdown("---")
st.caption("Built by Kaustubh Patil🚀")