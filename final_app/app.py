iimport streamlit as st
import sys
import os
import re

# FIX PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_agent import run_multi_agent_system
from backend.resume_parser import extract_text_from_pdf
from backend.live_job_fetcher import fetch_live_jobs
from backend.build_job_embeddings import build_embeddings

# PAGE CONFIG
st.set_page_config(
    page_title="AI Career Intelligence System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SESSION STATE
if "jobs_refreshed" not in st.session_state:
    st.session_state.jobs_refreshed = False

if "last_error" not in st.session_state:
    st.session_state.last_error = None

# CUSTOM CSS
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

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

.section-heading {
    font-size: 26px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 14px;
}

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

.advice-card {
    background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
    padding: 26px;
    border-radius: 22px;
    border: 1px solid #1f2937;
    color: white;
    line-height: 1.75;
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
}

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

.footer {
    color: #94a3b8;
    text-align: center;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# HELPERS
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
        top_col, action_col = st.columns([4, 1])

        with top_col:
            st.subheader(f"{index}. {title}")
            st.markdown(f"**{company}** — {location}")

        with action_col:
            if url and url != "#":
                st.link_button("Apply Now", url, use_container_width=True)
            else:
                st.warning("No link")

        st.metric("Match", f"{match_percentage}%")
        st.progress(min(match_percentage / 100, 1.0))

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Match Level", match_level)

        with metric_col2:
            st.metric("AI Similarity", semantic_score)

        with metric_col3:
            st.metric("Skill Matches", skill_score)

        st.markdown("**Matched Skills**")
        render_skill_pills(matched_skills)

        st.markdown("**Why this matched:**")
        st.info(reason)


# HERO
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

# SIDEBAR
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

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Developer Options")
show_logs = st.sidebar.checkbox("Show AI System Logs", value=False)

resume_text = None

if uploaded_file:
    try:
        with st.sidebar.spinner("Reading resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        if resume_text and resume_text.strip():
            st.sidebar.success("Resume loaded successfully")
        else:
            st.sidebar.error("Resume text could not be extracted. Try another PDF.")

    except Exception as error:
        st.sidebar.error("Failed to read resume.")
        st.session_state.last_error = str(error)

# LIVE JOB REFRESH
if refresh_jobs:
    try:
        with st.spinner("Fetching fresh jobs from API..."):
            fresh_jobs = fetch_live_jobs(
                role=role,
                location=location,
                results_per_page=25
            )

        if not fresh_jobs:
            st.warning("No fresh jobs found. Try a broader role or location.")
        else:
            st.success(f"Fetched {len(fresh_jobs)} fresh jobs")

            with st.spinner("Rebuilding semantic job embeddings..."):
                build_embeddings()

            st.session_state.jobs_refreshed = True
            st.success("Job embeddings updated successfully")

    except Exception as error:
        st.error("Live job refresh failed. Please check API keys or try again.")
        st.session_state.last_error = str(error)

# MAIN CONTENT
st.markdown('<div class="section-heading">🧠 AI Career Analysis</div>', unsafe_allow_html=True)

if resume_text:
    with st.expander("📄 Resume Preview", expanded=False):
        render_resume_preview(resume_text)

    st.info("Tip: Refresh live jobs first for the newest job results, then run the AI analysis.")

    run_analysis = st.button("🚀 Run AI Analysis", use_container_width=True)

    if run_analysis:
        try:
            with st.spinner("Running multi-agent AI system..."):
                result = run_multi_agent_system(
                    resume_text,
                    role=role,
                    location=location,
                    top_n=top_n
                )

            # SUMMARY METRICS
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

            # JOB MATCHES
            st.markdown('<div class="section-heading">💼 Top Job Matches</div>', unsafe_allow_html=True)

            if result.top_jobs:
                for index, job in enumerate(result.top_jobs, start=1):
                    render_job_card(job, index)
            else:
                st.error("No jobs found. Try refreshing live jobs or changing filters.")

            # CAREER RECOMMENDATIONS
            st.markdown('<div class="section-heading">🎯 Career Recommendations</div>', unsafe_allow_html=True)

            formatted_advice = format_links(result.final_answer)

            st.markdown(
                f'<div class="advice-card">{formatted_advice}</div>',
                unsafe_allow_html=True
            )

            # LOGS
            if show_logs:
                with st.expander("🧠 Developer Logs"):
                    for log in result.logs:
                        st.write(log)

        except Exception as error:
            st.error("AI analysis failed. Please try again or refresh live jobs.")
            st.session_state.last_error = str(error)

else:
    st.info("Upload your resume from the sidebar to start your AI career analysis.")

# DEVELOPER ERROR DETAILS
if show_logs and st.session_state.last_error:
    with st.expander("🚨 Last Error"):
        st.code(st.session_state.last_error)

st.markdown("---")
st.markdown(
    '<div class="footer">🚀 Built by Kaustubh Patil | Multi-Agent AI Career Intelligence System</div>',
    unsafe_allow_html=True
)