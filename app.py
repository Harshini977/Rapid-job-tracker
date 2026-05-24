import streamlit as st
import os
from job_engine import JobRecommenderEngine

st.set_page_config(page_title="Job Tracker", layout="wide")
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Add GEMINI_API_KEY to Streamlit Secrets!")
    st.stop()

engine = JobRecommenderEngine(api_key)

st.title("⚡ Real-Time AI Job Tracker")
keyword = st.sidebar.text_input("Target Profile", "Java Developer")
location = st.sidebar.text_input("Location", "Hyderabad")

if st.sidebar.button("Execute Pipeline"):
    jobs = engine.fetch_jobs(keyword, location)
    st.metric("Total Jobs", len(jobs))
    
    for job in jobs:
        with st.container(border=True):
            st.subheader(f"{job['title']} at {job['company']}")
            if st.button(f"Draft Email for {job['job_id']}", key=job['job_id']):
                st.write(engine.generate_email(job, "Recruiter"))