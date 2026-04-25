import streamlit as st
import sys
import os
import re

# ==============================
# FIX PATH (IMPORTANT)
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================
# MULTI-AGENT SYSTEM (NEW)
# ==============================
from smart_agent import run_multi_agent_system

# Backend
from backend.resume_parser import (
    extract_text_from_pdf,
)

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

.card a {
    color: #4da3ff;
    text-decoration: none;
}

.card a:hover {
    text-decoration: underline;
}

.section-title {
    font-size: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HELPERS
# ==============================
def format_links(text):
    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        r'<a href="\2" target="_blank">\1</a>',
        text
    )
    return text.replace("\n", "<br>")


def format_card(text):
    return f"""
    <div class="card">
    {text}
    </div>
    """

# ==============================
# HEADER
# ==============================
st.title("🚀 AI Career Intelligence System")
st.markdown("Multi-Agent AI System for Jobs, Skills & Career Strategy")
st.markdown("---")

# ==============================
# SIDEBAR (INPUT)
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
        # FINAL OUTPUT
        # ==============================
        st.markdown("## 🎯 Career Recommendations")

        formatted = format_links(result_state.final_answer or "No output generated")
        st.markdown(format_card(formatted), unsafe_allow_html=True)

        # ==============================
        # DEBUG LOGS (VERY IMPRESSIVE)
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
