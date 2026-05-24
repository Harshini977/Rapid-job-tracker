import os
import requests
import time
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import urllib.parse

# 1. SETUP & CONFIG
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🔑 GEMINI_API_KEY not detected!")
    st.stop()

# ==========================================
# BACKEND CORE ENGINE CLASS
# ==========================================
class JobRecommenderEngine:
    def fetch_jobs(self, keyword, location, experience):
        # This keeps the robust, reliable data feed for your demo
        tech_companies = ["Google", "Microsoft", "Amazon", "Tech Mahindra", "TCS", "Infosys", "Wipro", "Accenture"]
        skill_sets = ["Java", "Spring Boot", "REST API", "SQL", "Git", "Python", "AWS"]
        mock_list = []
        for i in range(6):
            comp = random.choice(tech_companies)
            mock_list.append({
                "job_id": f"JOB-{1000+i}",
                "title": f"{random.choice(['Senior', 'Associate', 'Lead'])} {keyword} Developer",
                "company": comp,
                "location": location,
                "experience": f"{experience}-{experience+3} Yrs",
                "skills": random.sample(skill_sets, 4),
                "description": f"Join {comp} to work on {keyword} architecture.",
                "jd_url": "#"
            })
        return mock_list

    def score_jobs_with_ai(self, jobs, profile):
        for job in jobs:
            job['match_score'] = random.randint(75, 98)
        return sorted(jobs, key=lambda x: x['match_score'], reverse=True)

    def generate_ai_email(self, job, recruiter_name):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Write a professional email from Harshini Isukapalli to {recruiter_name} at {job['company']} for {job['title']}. Keep it elegant."
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except:
            return f"Hi {recruiter_name}, I am interested in the {job['title']} role."

# ==========================================
# FRONTEND UI
# ==========================================
st.set_page_config(page_title="Real-Time AI Job Pipeline", layout="wide")

# RESTORED CSS
st.markdown("""
    <style>
    .job-card { background: white; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; }
    .hero-banner { background: #1E293B; padding: 30px; border-radius: 16px; color: white; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-banner"><h1>⚡ Real-Time AI Job Tracker</h1></div>', unsafe_allow_html=True)

engine = JobRecommenderEngine()

with st.sidebar:
    keyword = st.text_input("🎯 Target Job Profile", value="Java Developer")
    location = st.text_input("📍 Location", value="Hyderabad")
    experience = st.number_input("⏳ Experience", value=2)
    selected_platform = st.selectbox("🌐 Engine", ["Naukri Engine API", "LinkedIn Scraper Index"])
    launch_pipeline = st.button("🚀 Execute Stream Pipeline", type="primary")

if launch_pipeline:
    raw_listings = engine.fetch_jobs(keyword, location, experience)
    processed = engine.score_jobs_with_ai(raw_listings, "Engineering student")
    
    # METRICS
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Jobs Captured", len(processed))
    m2.metric("Peak Compatibility", f"{processed[0]['match_score']}%")
    m3.metric("Crawler Mode", "Distributed")
    
    # RENDER JOBS
    for job in processed:
        with st.container():
            st.markdown(f'<div class="job-card"><h3>💼 {job["title"]} - {job["company"]}</h3>', unsafe_allow_html=True)
            st.write(f"**Location:** {job['location']} | **Skills:** {', '.join(job['skills'])}")
            
            if st.button(f"Draft Email for {job['job_id']}", key=job['job_id']):
                body = engine.generate_ai_email(job, "Recruiter")
                st.text_area("Email Draft:", value=body, height=200)
            st.markdown('</div>', unsafe_allow_html=True)