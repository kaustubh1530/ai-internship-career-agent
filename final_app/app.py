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
from backend.live_job_fetcher import fetch_live_jobs
from backend.build_job_embeddings import build_embeddings

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Career Intelligence System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
/* Main page spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e293b 100%);
    padding: 34px;
    border-radius: 24px;
    border: 1px solid #1f2937;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

.hero-title {
    font-size: 44px;
    font-weight: 850;
    margin-bottom: 8px;
    color: white;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 18px;
    line-height: 1.6;
    max-width: 950px;
}

/* Section header */
.section-heading {
    font-size: 26px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 14px;
}

/* Small feature badges */
.badge {
    display: inline-block;
    background-color: #1d4ed8;
    color: white;
    padding: 7px 12px;
    border-radius: 999px;
    margin-right: 8px;
    margin-top: 12px;
    font-size: 13px;
    font-weight: 650;
}

/* Job cards */
.job-card {
    background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
    border: 1px solid #1f2937;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
}

.job-title {
    font-size: 23px;
    font-weight: 750;
    color: white;
    margin-bottom: 4px;
}

.company-line {
    color: #cbd5e1;
    font-size: 15px;
    margin-bottom: 16px;
}

.match-chip {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background-color: #2563eb;
    color: white;
    font-weight: 750;
    font-size: 13px;
    margin-right: 8px;
    margin-bottom: 10px;
}

.match-chip-green {
    background-color: #047857;
}

.match-chip-yellow {
    background-color: #b45309;
}

.reason-box {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 14px;
    margin-top: 14px;
    color: #e5e7eb;
    font-size: 14px;
    line-height: 1.55;
}

/* Skill pills */
.skill-pill {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background-color: #064e3b;
    color: #d1fae5;
    font-size: 13px;
    margin-right: 6px;
    margin-top: 6px;
}

/* Career advice card */
.advice-card {
    background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
    padding: 26px;
    border-radius: 22px;
    border: 1px solid #1f2937;
    color: white;
    line-height: 1.75;
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
}

/* Resume preview */
.resume-box {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 16px;
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.5;
    max-height: 230px;
    overflow-y: auto;
}

/* Footer */
.footer {
    color: #94a3b8;
    text-align: center;
    margin-top: 30px;
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
        r'<a href="\\2" target="_blank">\\1</a>',
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


def get_match_chip_class(match_percentage):
    if match_percentage >= 70:
        return "match-chip match-chip-green"
    if match_percentage >= 40:
        return "match-chip match-chip-yellow"
    return "match-chip"


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

    chip_class = get_match_chip_class(match_percentage)

    with st.container():
        st.markdown('<div class="job-card">', unsafe_allow_html=True)

        top_col, action_col = st.columns([4, 1])

        with top_col:
            st.markdown(
                f"""
                <div class="job-title">{index}. {title}</div>
                <div class="company-line"><b>{company}</b> — {location}</div>
                """,
                unsafe_allow_html=True
            )

        with action_col:
            if url and url != "#":
                st.link_button("Apply Now", url, use_container_width=True)
            else:
                st.warning("No link")

        st.markdown(
            f"""
            <span class="{chip_class}">{match_percentage}% Match</span>
            <span class="match-chip">{match_level}</span>
            """,
            unsafe_allow_html=True
        )

        st.progress(min(match_percentage / 100, 1.0))

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("AI Similarity", semantic_score)

        with metric_col2:
            st.metric("Skill Matches", skill_score)

        with metric_col3:
            st.metric("Final Score", job.get("score", 0))

        st.markdown("**Matched Skills**")
        render_skill_pills(matched_skills)

        st.markdown(
            f"""
            <div class="reason-box">
                <b>Why this matched:</b><br>
                {reason}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


def render_resume_preview(resume_text):
    if not resume_text:
        st.warning("No resume text found.")
        return

    st.text_area(
        label="Parsed Resume Text",
        value=resume_text,
        height=400,
        disabled=True
    )


# ==============================
# HERO
# ==============================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🚀 AI Career Intelligence System</div>
        <div class="hero-subtitle">
            Upload your resume, refresh live jobs, and get semantic AI-powered job matches with career recommendations.
            Built with multi-agent orchestration, embeddings, memory, and explainable matching.
        </div>
        <span class="badge">Multi-Agent AI</span>
        <span class="badge">Semantic Matching</span>
        <span class="badge">Live Jobs</span>
        <span class="badge">Career Strategy</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("👤 Resume")
uploaded_file = st.sidebar.file_uploader("Upload Resume PDF", type=["pdf"])

st.sidebar.markdown("---")
st.sidebar.header("🔍 Job Preferences")

role = st.sidebar.text_input(
    "Target Role",
    value="Software Engineering Intern",
    placeholder="Example: Software Engineer Intern"
)

location = st.sidebar.text_input(
    "Preferred Location",
    value="Maryland",
    placeholder="Example: Remote, Maryland"
)

top_n = st.sidebar.slider("Number of Jobs", 3, 10, 3)

st.sidebar.markdown("---")
st.sidebar.header("🌐 Live Job Data")

refresh_jobs = st.sidebar.button("🔄 Refresh Live Jobs", use_container_width=True)

resume_text = None

if uploaded_file:
    with st.sidebar.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.sidebar.success("Resume loaded successfully")

# ==============================
# LIVE JOB REFRESH
# ==============================
if refresh_jobs:
    try:
        with st.spinner("Fetching fresh jobs from API..."):
            fresh_jobs = fetch_live_jobs(
                role=role,
                location=location,
                results_per_page=25
            )

        st.success(f"Fetched {len(fresh_jobs)} fresh jobs")

        with st.spinner("Rebuilding semantic job embeddings..."):
            build_embeddings()

        st.success("Job embeddings updated successfully")

    except Exception as error:
        st.error(f"Job refresh failed: {error}")

# ==============================
# MAIN CONTENT
# ==============================
st.markdown('<div class="section-heading">🧠 AI Career Analysis</div>', unsafe_allow_html=True)

if resume_text:
    with st.expander("📄 Resume Preview", expanded=False):
        render_resume_preview(resume_text)

    run_analysis = st.button("🚀 Run AI Analysis", use_container_width=True)

    if run_analysis:
        with st.spinner("Running multi-agent AI system..."):
            result = run_multi_agent_system(
                resume_text,
                role=role,
                location=location,
                top_n=top_n
            )

        # ==============================
        # SUMMARY METRICS
        # ==============================
        st.markdown('<div class="section-heading">📊 Analysis Summary</div>', unsafe_allow_html=True)

        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

        with summary_col1:
            st.metric("Jobs Returned", len(result.top_jobs))

        with summary_col2:
            st.metric("Skills Found", len(result.extracted_skills))

        with summary_col3:
            best_match = result.top_jobs[0].get("match_percentage", 0) if result.top_jobs else 0
            st.metric("Best Match", f"{best_match}%")

        with summary_col4:
            st.metric("Agents Used", "4+")

        # ==============================
        # JOB MATCHES
        # ==============================
        st.markdown('<div class="section-heading">💼 Top Job Matches</div>', unsafe_allow_html=True)

        if result.top_jobs:
            for index, job in enumerate(result.top_jobs, start=1):
                render_job_card(job, index)
        else:
            st.error("No jobs found. Try refreshing live jobs or changing filters.")

        # ==============================
        # CAREER RECOMMENDATIONS
        # ==============================
        st.markdown('<div class="section-heading">🎯 Career Recommendations</div>', unsafe_allow_html=True)

        formatted_advice = format_links(result.final_answer)

        st.markdown(
            f'<div class="advice-card">{formatted_advice}</div>',
            unsafe_allow_html=True
        )

        # ==============================
        # LOGS
        # ==============================
        with st.expander("🧠 View AI System Logs"):
            for log in result.logs:
                st.write(log)

else:
    st.info("Upload your resume from the sidebar to start your AI career analysis.")

st.markdown("---")
st.markdown(
    '<div class="footer">🚀 Built by Kaustubh Patil | Multi-Agent AI Career Intelligence System</div>',
    unsafe_allow_html=True
)