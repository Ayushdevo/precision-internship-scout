import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from jobs import fetch_vetted_jobs
from rendering import render_job_card, safe_careers_url

# Load environment variables
load_dotenv()

# Initialize Streamlit Page configuration for a sleek dark executive dashboard
st.set_page_config(
    page_title="Precision Internship Scout",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling via CSS injection to elevate visual aesthetics
# Overriding defaults for a sleek, premium, glassmorphism-inspired executive layout
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">

<style>
    /* Global Typography & Custom Styling */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    code, pre, [class*="mono"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Executive Main Header Style */
    .main-header-container {
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .main-title {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a5b4fc, #6366f1, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin: 0;
    }
    .main-subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* Sidebar Title & Glass Effect */
    .sidebar-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Secure Local Vault Badge */
    .vault-badge {
        font-size: 0.75rem;
        background-color: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 2px 8px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 1rem;
        display: inline-block;
    }
    
    .resume-badge {
        font-size: 0.75rem;
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        margin-top: 0.5rem;
        display: inline-block;
    }

    /* Deploy Agent Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        cursor: pointer !important;
        margin-bottom: 2rem !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Vetted Job Listing Cards */
    .job-card {
        background: rgba(24, 24, 37, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .job-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.12);
    }
    
    .job-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .job-card-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }

    .job-card-meta {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 0.25rem;
        margin-bottom: 1rem;
    }

    /* Score Tags */
    .match-tag {
        font-size: 0.85rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 30px;
        text-align: center;
    }
    .match-tag-success {
        background-color: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .match-tag-info {
        background-color: rgba(59, 130, 246, 0.12);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .match-tag-warning {
        background-color: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Requirements tags */
    .req-badge {
        display: inline-block;
        font-size: 0.75rem;
        background-color: rgba(255, 255, 255, 0.05);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2px 8px;
        border-radius: 6px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .apply-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: rgba(255, 255, 255, 0.03);
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        border-radius: 6px;
        text-decoration: none !important;
        transition: all 0.2s ease;
        margin-top: 1rem;
    }
    .apply-btn:hover {
        background-color: rgba(255, 255, 255, 0.08);
        border-color: rgba(99, 102, 241, 0.5);
    }
</style>
""", unsafe_allow_html=True)

from resume import extract_resume_text as parse_resume


def extract_resume_text(uploaded_file) -> str:
    try:
        return parse_resume(uploaded_file)
    except ValueError as exc:
        st.sidebar.error(str(exc))
        return ""

from scoring import compute_dynamic_match, build_profile_text

# 1. FIXED SIDEBAR - Candidate Profile (Secure Local Data Vault)
with st.sidebar:
    st.markdown('<div class="sidebar-title">🔒 Candidate Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="vault-badge">Session profile</div>', unsafe_allow_html=True)
    
    # Pre-filled credentials per specification
    candidate_name = st.text_input(
        "Name", 
        value="Ayush Tiwari",
        key="vault_candidate_name"
    )
    
    candidate_univ = st.text_input(
        "University", 
        value="IIT Guwahati (Class of 2028)",
        key="vault_candidate_university"
    )
    
    candidate_target = st.text_input(
        "Target", 
        value="AI Engineer Intern (2026)",
        key="vault_candidate_target"
    )
    
    role_keyword = st.text_input("Search keyword", value="AI", key="search_keyword")

    # Comma-separated text area for core skills
    candidate_skills = st.text_area(
        "Core Skills",
        value="Python, PyTorch, JAX, Hugging Face Transformers, LLMs, RAG, LangChain, LlamaIndex, vLLM, Vector Databases, Docker, Git",
        height=140,
        key="vault_candidate_skills"
    )
    
    # Resume file uploader (PDF / TXT supported)
    resume_file = st.file_uploader(
        "Upload Resume (PDF, TXT)", 
        type=["pdf", "txt"], 
        key="vault_candidate_resume"
    )
    
    resume_text = ""
    # Look for local sample_resume.txt as a fallback to auto-populate the local vault
    sample_path = Path(__file__).with_name("sample_resume.txt")
    use_sample = st.checkbox("Use bundled demo resume", value=False, key="use_sample_resume")
    auto_loaded = False
    
    if resume_file is not None:
        resume_text = extract_resume_text(resume_file)
        st.markdown(f'<div class="resume-badge">📄 Resume Vault Loaded ({len(resume_text)} chars)</div>', unsafe_allow_html=True)
    elif use_sample and sample_path.exists():
        try:
            with open(sample_path, "r", encoding="utf-8") as f:
                resume_text = f.read()
                auto_loaded = True
            st.markdown(f'<div class="resume-badge" style="background-color: rgba(99,102,241,0.15); color: #818cf8; border-color: rgba(99,102,241,0.3);">📄 Demo Resume ({len(resume_text)} chars)</div>', unsafe_allow_html=True)
        except Exception:
            pass
    
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; line-height: 1.4;">
        <strong>Session privacy:</strong> Resume text is processed on the Streamlit server. On a hosted deployment, uploads leave your device. The app does not intentionally save uploaded resumes to disk.
        </div>
        """,
        unsafe_allow_html=True
    )

# 2. MAIN LAYOUT STAGE
st.markdown(
    """
    <div class="main-header-container">
        <h1 class="main-title">🤖 Precision Internship Scout</h1>
        <p class="main-subtitle">Bypass the noise. Find the perfect tech match.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Render a beautiful introduction card explaining the multi-agent system
st.info(
    "Demo mode: these are illustrative sample listings, not verified live vacancies. "
    "Scores reflect keyword overlap with your profile, not hiring probability. "
    "The app does not submit applications."
)

# Compile candidate profile text for dynamic scoring
combined_profile_text = build_profile_text(candidate_skills, resume_text)

# Wide Primary Action Button
deploy_button = st.button("Search sample listings", key="btn_deploy_scout")

if deploy_button:
    with st.status("Searching sample listings...", expanded=True) as status:
        vetted_listings = fetch_vetted_jobs(role_keyword)
        st.write(f"Found {len(vetted_listings)} illustrative listings.")
        status.update(label="Sample search complete", state="complete", expanded=False)

    st.session_state["scout_jobs"] = vetted_listings
    st.session_state["scout_query"] = role_keyword.strip().casefold()

if st.session_state.get("scout_query") != role_keyword.strip().casefold():
    st.session_state.pop("scout_jobs", None)

if "scout_jobs" in st.session_state:
    st.success("Sample search complete. Review the illustrative matches below:")

    # 4. RENDER VETTED JOB MATCH CARDS
    # We define the deterministic mock data attributes and ratings as requested by the specification
    # We calculate the scores dynamically based on actual skill match overlaps!
    jobs_to_assess = st.session_state["scout_jobs"]
    if not jobs_to_assess:
        st.info("No sample listings match this keyword. Try Python, AI, or Research.")

    # Render clean stacked containers
    for job in jobs_to_assess:
        # Dynamically compute the score & match lists
        score, matched_reqs, missing_reqs = compute_dynamic_match(job["requirements"], combined_profile_text, 0)
        
        # Classify badge colors and warnings based on calculated score
        if score >= 90:
            badge_class = "match-tag-success"
            severity = "success"
        elif score >= 75:
            badge_class = "match-tag-info"
            severity = "info"
        else:
            badge_class = "match-tag-warning"
            severity = "warning"
            
        with st.container():
            st.markdown(render_job_card(job, score, matched_reqs), unsafe_allow_html=True)

            # Construct dynamic assessor explanation
            matched_str = ", ".join(matched_reqs) if matched_reqs else "None"
            missing_str = ", ".join(missing_reqs) if missing_reqs else "None"
            
            verdict_text = (
                f"**Keyword coverage:** {len(matched_reqs)} of {len(job['requirements'])} requirements matched.\n\n"
                f"**Matched keywords:** {matched_str}\n\n"
                f"**Keywords not found:** {missing_str}"
            )
            
            # Use color highlight blocks matching the severity of the match score
            if severity == "success":
                st.success(verdict_text)
            elif severity == "info":
                st.info(verdict_text)
            elif severity == "warning":
                st.warning(verdict_text)
                
            link = safe_careers_url(job["target_link"])
            if link:
                st.link_button("Open sample careers link", link)

            st.write("") # Spacer between containers
            st.write("---")

else:
    st.write("👈 Upload your resume and configure profile details in the Secure Local Data Vault, then search the sample listings.")
