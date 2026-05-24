import os
import requests
import time
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import urllib.parse
from job_engine import JobRecommenderEngine

# Configure the Gemini API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🔑 API Key not found!")
    st.stop()

# Load UI and Engine
st.set_page_config(page_title="Real-Time AI Job Pipeline", layout="wide")
engine = JobRecommenderEngine()

# --- CSS STYLING ---
st.markdown("""
    <style>
    .job-card { background: white; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; }
    .hero-banner { background: #1E293B; padding: 30px; border-radius: 16px; color: white; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-banner"><h1>⚡ Real-Time AI Job & HR Tracker</h1></div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    keyword = st.text_input("Target Job Profile", "Java Developer")
    location = st.text_input("Location", "Hyderabad")
    experience = st.number_input("Experience (Years)", value=2)
    selected_platform = st.selectbox("Engine", ["Naukri Engine API", "LinkedIn Scraper Index"])
    launch_pipeline = st.button("🚀 Execute Stream Pipeline", type="primary")

# --- MAIN LOGIC ---
if launch_pipeline:
    raw_listings = engine.fetch_jobs(keyword, location, experience)
    processed = engine.score_jobs_with_ai(raw_listings, "Engineering student")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Jobs Captured", len(processed))
    m2.metric("Peak Compatibility", f"{processed[0]['match_score']}%")
    
    for job in processed:
        with st.container():
            st.markdown(f'<div class="job-card"><h3>💼 {job["title"]} - {job["company"]}</h3>', unsafe_allow_html=True)
            st.write(f"**Location:** {job['location']}")
            if st.button(f"Draft Email for {job['job_id']}", key=job['job_id']):
                st.write(engine.generate_ai_email(job, "Recruiter"))
            st.markdown('</div>', unsafe_allow_html=True)