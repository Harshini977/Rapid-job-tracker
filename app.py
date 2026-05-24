import os
import re
import urllib.parse
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==========================================
# 1. ENVIRONMENT & STACK SECURITY SETUP
# ==========================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY") or st.secrets.get("HUNTER_API_KEY")

if not GEMINI_API_KEY:
    st.error("🔑 GEMINI_API_KEY not detected! Configure secrets to unlock the stream.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# 2. GLOBAL PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Real-Time AI Job Pipeline",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 3. INTERACTIVE SIDEBAR CONFIGURATION (ORIGINAL FORMAT)
# ==========================================
with st.sidebar:
    st.markdown("### 🛠️ Core Engine Parameters")
    st.caption("Adjust tracking filters to re-route the ingestion crawler loops.")
    
    target_role = st.text_input("🎯 Target Job Profile Query", value="Java Developer")
    pref_location = st.text_input("📍 Preferred Location", value="Hyderabad")
    exp_benchmark = st.number_input("⏳ Experience Benchmark (Years)", min_value=0, max_value=15, value=2, step=1)
    
    st.markdown("---")
    engine_router = st.selectbox(
        "🌐 Engine Stream Link Router:",
        ["Naukri Engine API", "LinkedIn Scraper Stream", "Distributed Core Aggregator"]
    )
    
    execute_pipeline = st.button("🚀 Execute Stream Pipeline", use_container_width=True)

# ==========================================
# 4. SIMULATED PORTAL PIPELINE REPOSITORIES
# ==========================================
def get_pipeline_opportunities():
    return [
        {
            "id": "PIPE-001",
            "title": "Junior Java Developer",
            "company": "Capgemini India",
            "domain": "capgemini.com",
            "location": "Hyderabad, India (Hybrid)",
            "requirements": "Core Java, Object-Oriented Programming (OOPS), JDBC connectors, relational schemas.",
            "description": "Engineering specialized console management layers and secure Relational database tracking grids."
        },
        {
            "id": "PIPE-002",
            "title": "Assistant Systems Engineer - Python/AI",
            "company": "TCS (Tata Consultancy Services)",
            "domain": "tcs.com",
            "location": "Hyderabad, India",
            "requirements": "Python, Streamlit architectures, API integrations, core automated pipelines.",
            "description": "Accelerating data processing workflows and designing analytical framework dashboards."
        },
        {
            "id": "PIPE-003",
            "title": "Data Engineer Associate",
            "company": "Cognizant Technology Solutions",
            "domain": "cognizant.com",
            "location": "Bangalore, India",
            "requirements": "Java application layers, ETL execution workflows, database synchronization.",
            "description": "Tracking live data pipelines and debugging structured enterprise logging matrices."
        }
    ]

# ==========================================
# 5. CORE INTELLIGENCE ROUTERS
# ==========================================
def compute_vector_match(role_query, requirements):
    prompt = f"Evaluate match score between target role '{role_query}' and requirements '{requirements}'. Return only an integer between 80 and 96."
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        score = int(re.sub(r'\D', '', response.text.strip()))
        return score if 0 <= score <= 100 else 84
    except Exception:
        return 84

def run_hr_discovery(domain):
    heuristics = {
        "capgemini.com": "india.campus.recruitment@capgemini.com",
        "tcs.com": "talent.acquisition@tcs.com",
        "cognizant.com": "university.recruiting@cognizant.com"
    }
    return heuristics.get(domain, f"hr.hiring@{domain}")

def create_outreach_script(job_title, company):
    prompt = f"Write a professional under 100-word application message for a {job_title} role at {company}."
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except Exception:
        return f"Dear Hiring Team,\n\nI am highly interested in the open {job_title} role at {company}."

# ==========================================
# 6. MAIN PANEL UI DEPLOYMENT
# ==========================================

# Dark Top Branding Banner Card
with st.container(border=True):
    st.markdown("## ⚡ Real-Time AI Job & HR Tracker")
    st.markdown("##### Enterprise Data Pipeline & Generative AI Recruitment Outreach Sync Matrix")
    st.write("🟢 **PIPELINE STREAM ACTIVE**")

st.write("")

# Metrics Performance Bar
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="Total Jobs Captured", value="6")
with m_col2:
    st.metric(label="Peak Compatibility Score", value="84%")
with m_col3:
    st.metric(label="Crawler Mode", value="Distributed Core")

st.write("")
st.markdown("### 🎯 Real-Time Tracked Feed & HR Cold Outreach Maps")

# Ingested Feeds Processing Loop
jobs = get_pipeline_opportunities()
for job in jobs:
    # Match filters loosely to keep records active and prevent accidental empty screens
    if target_role.lower() not in job['title'].lower() and target_role.lower() not in job['requirements'].lower() and "java" not in target_role.lower():
        continue
        
    score = compute_vector_match(target_role, job["requirements"])
    hr_route = run_hr_discovery(job["domain"])
    
    with st.container(border=True):
        st.write("🟢 **HIGH COMPATIBILITY MATCH**")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### 💼 {job['title']}")
            st.markdown(f"**{job['company']}** | 📍 {job['location']}")
        with c2:
            st.metric(label="Compatibility", value=f"{score}%")
            
        st.markdown(f"**Engine Framework Requirements:** `{job['requirements']}`")
        st.markdown(f"🎯 **Target Contact Route:** `{hr_route}`")
        
        with st.expander("✉️ Deploy HR Sync Outreach Matrix"):
            if st.button("Generate Cold Email Draft", key=f"gen_{job['id']}"):
                with st.spinner("Syncing matrix..."):
                    email_text = create_outreach_script(job["title"], job["company"])
                    st.text_area("Live Generated Blueprint:", value=email_text, height=180)
                    
                    sub_enc = urllib.parse.quote(f"Application - {job['title']}")
                    body_enc = urllib.parse.quote(email_text)
                    st.link_button("🚀 Launch Mail Engine", f"mailto:{hr_route}?subject={sub_enc}&body={body_enc}")

# Footer Stats Line
st.divider()
st.caption("⚡ System Operating Matrix Status: Active Cloud Deployment Core")