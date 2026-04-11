import streamlit as st
from hybrid_search import hybrid_search

st.set_page_config(page_title="AI Career Agent", layout="wide")

st.title("🚀 AI Internship Career Agent")

query = st.text_input("Enter job search query (e.g., AI internship)")
skills = st.text_input("Enter your skills (comma-separated)")

if st.button("Find Jobs"):
    user_skills = [s.strip().lower() for s in skills.split(",")]

    results = hybrid_search(query, user_skills)

    st.subheader("Top Matches")

    for res in results:
        job = res["job"]

        st.markdown(f"### {job['title']}")
        st.write(f"Company: {job['company']}")
        st.write(f"Location: {job['location']}")
        st.write(f"Match Score: {res['score']}%")
        st.write(f"Matched Skills: {res['matched']}")
        st.markdown(f"[Apply Here]({job['url']})")

        st.markdown("---")