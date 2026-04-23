import streamlit as st
import sys
import os

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================
# LANGCHAIN SYSTEM
# ==============================
from ai_langchain.smart_agent import run_smart_agent
from ai_langchain.context import set_user_skills

# Backend
from backend.resume_parser import (
    extract_text_from_pdf,
    extract_skills_from_text
)

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Career Agent",
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
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.title("🚀 AI Career Agent (LangChain Powered)")
st.markdown("AI-powered career assistant with reasoning + tools")
st.markdown("---")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("👤 Your Profile")

skills_input = st.sidebar.text_area(
    "Your Skills",
    placeholder="Python, SQL, FastAPI"
)

uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ==============================
# SKILLS HANDLING
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
# SET CONTEXT (IMPORTANT)
# ==============================
if user_skills:
    set_user_skills(user_skills)

# ==============================
# PROFILE DISPLAY
# ==============================
st.markdown("## 👤 Your Profile")

if user_skills:
    st.success(", ".join(user_skills))
else:
    st.warning("No skills provided")

# ==============================
# AI INTERACTION
# ==============================
st.markdown("## 💬 AI Career Assistant")

user_query = st.text_input(
    "Ask anything (jobs, skills, career advice)",
    placeholder="Find backend jobs for me and tell me if I should apply"
)

if user_query:
    with st.spinner("🤖 Thinking..."):
        response = run_smart_agent(user_query)

    st.markdown("## 🤖 AI Response")
    st.success(response)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built by Kaustubh Patil | AI Career Agent")