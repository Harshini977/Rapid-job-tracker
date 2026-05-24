# ⚡ Real-Time AI Job & HR Tracker

An enterprise-grade data pipeline and Generative AI recruitment outreach matrix built using Python, Streamlit, and the Google GenAI SDK.

## 🚀 Core Features
- **Live Job Processing:** Simulates multi-source ingestion pipelines targeting developer roles.
- **Contextual Alignment Engine:** Leverages automated vector-matching logic to score candidate profiles against incoming jobs.
- **Information Extraction (IE) Agent:** Utilizes **Hunter.io API data structure patterns** and heuristic logic to dynamically discover corporate HR email routes.
- **Automated Outreach Generation:** Integrates the modern `google-genai` SDK (`gemini-1.5-flash`) to generate human-aligned, personalized cold emails.

## 🛠️ Tech Stack
- **Frontend UI:** Streamlit (HTML/CSS injection layout)
- **AI Core:** Google GenAI SDK (`gemini-1.5-flash`)
- **Data Routines:** Python `requests`, `urllib`, `.env` state tracking

## ⚙️ Setup Instructions
1. Clone this repository.
2. Install dependencies: `pip install streamlit google-genai python-dotenv requests`
3. Create a `.env` file in the root directory and append your configurations:
   ```text
   GEMINI_API_KEY=AIzaSyDBiztVaaDkoe6exgfMmKsA9vZ_e-cR9bY
   HUNTER_API_KEY=hunter_demo_activated_2026 