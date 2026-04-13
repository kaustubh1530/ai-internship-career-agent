import streamlit as st
import sys
import os

# ==============================
# FIX PATH
# ==============================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.search_jobs import search
from backend.resume_parser import extract_text_from_pdf, extract_skills_from_text

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

# Ignore low-value tools
IGNORE_SKILLS = [
    "vs code", "postman", "jupyter", "git", "github"
]

# ==============================
# RESUME PROCESSING
# ==============================
if uploaded_file:

    with st.sidebar.spinner("📄 Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.sidebar.spinner("🧠 Extracting skills using AI..."):
        extracted_skills = extract_skills_from_text(resume_text)

    # Filter + limit skills
    extracted_skills = [s for s in extracted_skills if s not in IGNORE_SKILLS]
    user_skills = extracted_skills[:10]   # limit to top 10

    st.sidebar.success("✅ Skills extracted from resume")

    st.sidebar.markdown("### 🧠 Extracted Skills")
    st.sidebar.write(", ".join(user_skills))


# ==============================
# SKILL MATCHING LOGIC
# ==============================
skill_aliases = {
    "machine learning": ["ml"],
    "artificial intelligence": ["ai"],
    "python": ["python3"],
    "sql": ["mysql", "postgres", "database"],
    "embedding": ["embeddings"],
    "openapi": ["api", "rest api", "fastapi"],
    "vector search": ["faiss", "similarity search"],
}

def is_skill_match(skill, text):

    if skill in text:
        return True

    if skill in skill_aliases:
        for alias in skill_aliases[skill]:
            if alias in text:
                return True

    words = skill.split()
    return any(word in text for word in words)


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

    # ==============================
    # DISPLAY JOBS
    # ==============================
    for job in jobs:

        job_text = (
            job.get("title", "") + " " +
            job.get("description", "")
        ).lower()

        from backend.resume_parser import ai_match_skills

        matched = ai_match_skills(user_skills, job_text)
        
        # cleaner missing logic
        if len(matched) >= 2:
            missing = [skill for skill in user_skills if skill not in matched][:5]
        else:
            missing = []

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
            # SKILL MATCH
            # ==============================
            st.markdown("#### 🧠 Skill Match")

            col3, col4 = st.columns(2)

            with col3:
                st.markdown("**✅ Matched Skills**")
                st.success(", ".join(matched))

            with col4:
                st.markdown("**❌ Missing Skills**")
                if missing:
                    st.warning(", ".join(missing))
                else:
                    st.write("Looks like a strong match 🚀")

            # ==============================
            # INSIGHT
            # ==============================
            st.markdown("#### 💡 Why this matches you")

            if ai_match:
                st.info("Matched using AI semantic search (RAG).")
            else:
                st.info(f"Matched based on your skills: {', '.join(matched)}")

            # DESCRIPTION
            st.markdown("#### 📝 Description")
            st.write(job.get("description", "")[:250] + "...")

            # APPLY
            if job.get("url"):
                st.markdown(f"[👉 Apply Here]({job['url']})")

            st.markdown("</div>", unsafe_allow_html=True)