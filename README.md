# 🎯 Precision Internship Scout (Concierge Track)

An automated, multi-agent pipeline designed to discover, vet, and score 2026 AI/ML engineering internships for premium technical candidate profiles, bypassing noisy, low-tier recruitment aggregators.

## 🧠 Architecture & Multi-Agent Design
The system uses three core components:
1. **Orchestrator Agent:** Parses user intent and initializes the search parameters.
2. **Scout Agent:** Connects securely to the MCP server to pull clean JSON data from verified endpoints.
3. **Assessor Agent:** Evaluates the technical requirements of the job against the user's localized academic profile.

## 📚 Key Course Concepts Applied
1. **Multi-Agent System (ADK):** Divided workflows into an Orchestrator/Scout/Assessor structure to minimize hallucination.
2. **Model Context Protocol (MCP):** Implemented an MCP tool (`mcp_server.py`) to source highly structured JSON payloads.
3. **Security Features:** Localized candidate profiles remain on the user's machine. API keys are decoupled via `.env` files.
4. **Antigravity:** Deployed a frictionless, "vibe-coded" Streamlit UI (`app.py`) for a premium Concierge experience.

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone [https://github.com/Ayushdevo/precision-internship-scout.git](https://github.com/Ayushdevo/precision-internship-scout.git)
cd precision-internship-scout

# 2. Install required frameworks
pip install -r requirements.txt

# 3. Set up environment parameters
# Create a .env file in the root directory and add:
# GEMINI_API_KEY= your_actual_api_key_here

# 4. Execute the Concierge UI
streamlit run app.py
