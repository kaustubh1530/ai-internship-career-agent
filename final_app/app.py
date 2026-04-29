import streamlit as st
import sys
import os
import re

# ==============================
# FIX PATH (IMPORTANT)
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================
# MULTI-AGENT SYSTEM
# ==============================
from smart_agent import run_multi_agent_system

# Backend
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
# UI STYLE
# ==============================
st.markdown("""
<style>
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #222;
    color: white;
    line-height: 1.6;
}

.job-card {
    background-color: #0f172a;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #1e293b;
    color: white;
}

a {
    color: #4da3ff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HELPERS
# ==============================
def format_text(text):
    if not text:
        return "No output generated"

    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        r'<a href="\2" target="_blank">\1</a>',
        text
    )
    return text.replace("\n", "<br>")


def render_card(text):
    return f"<div class='card'>{text}</div>"


def render_job(job):
    url = job.get("url")

    apply_button = (
        f'<a href="{url}" target="_blank">🔗 Apply Here</a>'
        if url and url != "#"
        else "<p style='color: gray;'>No application link available</p>"
    )

    return f"""
    <div class="job-card">
        <h3>{job.get('title', 'No Title')}</h3>
        <p><b>Company:</b> {job.get('company', 'Unknown')}</p>
        <p><b>Location:</b> {job.get('location', 'Remote')}</p>
        {apply_button}
    </div>
    """

# ==============================
# HEADER
# ==============================
st.title("🚀 AI Career Intelligence System")
st.markdown("Multi-Agent AI System for Jobs, Skills & Career Strategy")
st.markdown("---")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("👤 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume (PDF)", type=["pdf"]
)

resume_text = None

if uploaded_file:
    with st.sidebar.spinner("📄 Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.sidebar.success("✅ Resume loaded")

# ==============================
# MAIN SECTION
# ==============================
st.markdown("## 🧠 AI Career Analysis")

if resume_text:

    if st.button("🚀 Run AI Analysis"):

        with st.spinner("🤖 Running multi-agent system..."):
            result_state = run_multi_agent_system(resume_text)

        # ==============================
        # CAREER ADVICE
        # ==============================
        st.markdown("## 🎯 Career Recommendations")

        formatted = format_text(result_state.final_answer)
        st.markdown(render_card(formatted), unsafe_allow_html=True)

        # ==============================
        # JOBS SECTION (🔥 NEW FIX)
        # ==============================
        st.markdown("## 💼 Recommended Jobs")

        if hasattr(result_state, "top_jobs") and result_state.top_jobs:

            cols = st.columns(2)

            for i, job in enumerate(result_state.top_jobs):

                with cols[i % 2]:
                    st.markdown(render_job(job), unsafe_allow_html=True)

        else:
            st.warning("No jobs available to display yet.")

        # ==============================
        # LOGS
        # ==============================
        with st.expander("🧠 View AI System Logs"):
            for log in result_state.logs:
                st.write(log)

else:
    st.warning("Please upload your resume to start")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built by Kaustubh Patil | Multi-Agent AI Career System")