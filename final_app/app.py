import streamlit as st
import sys
import os

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Backend import
from backend.search_jobs import search

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
st.markdown("AI-powered job matching using RAG + FAISS + OpenAI embeddings")

st.markdown("---")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("🔍 Search Jobs")

query = st.sidebar.text_input(
    "Job Role",
    placeholder="e.g. Software Engineer Intern"
)

location = st.sidebar.text_input(
    "Location (optional)",
    placeholder="e.g. New York"
)

search_button = st.sidebar.button("Search Jobs 🚀")

# ==============================
# MAIN LOGIC
# ==============================
if search_button:

    if not query:
        st.warning("⚠️ Please enter a job role")
        st.stop()

    with st.spinner("Searching jobs using AI..."):

        jobs = search(query)

    st.success(f"Found {len(jobs)} matches")

    st.markdown("## 🎯 Top Matches")

    # ==============================
    # DISPLAY JOBS
    # ==============================
    for job in jobs:

        with st.container():

            st.markdown("### 💼 " + job.get("title", "No Title"))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("🏢 Company:", job.get("company", "N/A"))

            with col2:
                st.write("📍 Location:", job.get("location", "N/A"))

            with col3:
                st.write("⭐ Score:", round(job.get("score", 0), 2))

            st.markdown("#### 📝 Description")
            st.write(job.get("description", "")[:300] + "...")

            if job.get("url"):
                st.markdown(f"[👉 Apply Here]({job['url']})")

            st.markdown("---")