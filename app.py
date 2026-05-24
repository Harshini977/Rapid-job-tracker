import streamlit as st
import os
import random
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="Job Tracker", layout="wide")
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Add GEMINI_API_KEY to Streamlit Secrets!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. LOGIC
def fetch_mock_jobs(keyword, location):
    companies = ["Google", "Microsoft", "Amazon", "Wipro", "TCS", "Infosys"]
    return [{
        "job_id": f"J-{i}",
        "title": f"{random.choice(['Senior', 'Associate'])} {keyword}",
        "company": random.choice(companies),
        "location": location
    } for i in range(6)]

# 3. UI
st.title("⚡ Real-Time AI Job Tracker")
keyword = st.sidebar.text_input("Target Profile", "Java Developer")
location = st.sidebar.text_input("Location", "Hyderabad")

if st.sidebar.button("Execute Pipeline"):
    jobs = fetch_mock_jobs(keyword, location)
    st.metric("Total Jobs Captured", len(jobs))
    
    for job in jobs:
        with st.container(border=True):
            st.subheader(f"{job['title']} at {job['company']}")
            if st.button(f"Draft Email for {job['job_id']}", key=job['job_id']):
                prompt = f"Write a professional email for a {job['title']} role at {job['company']}."
                response = model.generate_content(prompt)
                st.write(response.text)