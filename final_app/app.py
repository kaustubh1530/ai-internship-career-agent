import streamlit as st
import sys
import os

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
st.markdown("AI-powered job matching using RAG + FAISS + OpenAI")

st.markdown("---")

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("🔍 Search Jobs")

query = st.sidebar.text_input("Job Role", placeholder="Software Engineer Intern")

skills_input = st.sidebar.text_area(
    "Your Skills",
    placeholder="Python, SQL, Machine Learning, Pandas"
)

search_button = st.sidebar.button("Search Jobs 🚀")

# ==============================
# SKILL NORMALIZATION
# ==============================
user_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]

# synonyms mapping (VERY IMPORTANT)
skill_aliases = {
    "machine learning": ["ml"],
    "artificial intelligence": ["ai"],
    "javascript": ["js"],
    "python": ["python3"],
    "sql": ["mysql", "postgres", "database"],
}

def is_skill_match(skill, text):
    # direct match
    if skill in text:
        return True

    # check aliases
    if skill in skill_aliases:
        for alias in skill_aliases[skill]:
            if alias in text:
                return True

    # partial word match
    words = skill.split()
    return any(word in text for word in words)

# ==============================
# MAIN LOGIC
# ==============================
if search_button:

    if not query:
        st.warning("⚠️ Please enter a job role")
        st.stop()

    with st.spinner("Running AI job matching..."):
        jobs = search(query)

    st.success(f"Found {len(jobs)} matches")
    st.markdown("## 🎯 Top Matches For You")

    # ==============================
    # DISPLAY JOBS
    # ==============================
    for job in jobs:

        # combine title + description (IMPORTANT FIX)
        job_text = (
            job.get("title", "") + " " +
            job.get("description", "")
        ).lower()

        # match skills
        matched = [skill for skill in user_skills if is_skill_match(skill, job_text)]
        missing = [skill for skill in user_skills if skill not in matched]

        # fallback if nothing matched
        ai_match = False
        if not matched:
            matched = ["Relevant (AI Match)"]
            ai_match = True

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

            # TITLE
            st.markdown(f"### 💼 {job.get('title', 'No Title')}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"🏢 **Company:** {job.get('company', 'N/A')}")
                st.write(f"📍 **Location:** {job.get('location', 'N/A')}")

            with col2:
                st.write(f"⭐ **Match Score:** {round(job.get('score', 0), 2)}")

            # ==============================
            # SKILL MATCH UI
            # ==============================
            st.markdown("#### 🧠 Skill Match")

            col3, col4 = st.columns(2)

            with col3:
                st.markdown("**✅ Matched Skills**")
                if matched:
                    st.success(", ".join(matched))
                else:
                    st.write("None")

            with col4:
                st.markdown("**❌ Missing Skills**")
                if missing:
                    st.error(", ".join(missing))
                else:
                    st.write("None")

            # ==============================
            # INSIGHT
            # ==============================
            st.markdown("#### 💡 Why this matches you")

            if ai_match:
                st.info("This job is matched using AI semantic search (RAG).")
            else:
                st.info(f"Matched based on your skills: {', '.join(matched)}")

            # ==============================
            # DESCRIPTION
            # ==============================
            st.markdown("#### 📝 Description")
            st.write(job.get("description", "")[:250] + "...")

            # APPLY
            if job.get("url"):
                st.markdown(f"[👉 Apply Here]({job['url']})")

            st.markdown("</div>", unsafe_allow_html=True)