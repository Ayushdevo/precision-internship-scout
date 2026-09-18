# Precision Internship Scout

A Streamlit demonstration that searches three illustrative job listings and compares
their requirement keywords with a supplied skills profile and resume. An optional
FastMCP adapter exposes the same local sample data as a tool.

## Data provenance

These listings and careers links are **not verified current vacancies**. Keyword
coverage is not a hiring probability. The app does not submit applications and does
not use an LLM or autonomous agents. No API key is required.

## Run locally

Use Python 3.11 or newer:

```bash
git clone https://github.com/Ayushdevo/precision-internship-scout.git
cd precision-internship-scout
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

To expose the sample source over MCP, run `python mcp_server.py`.

Resume processing occurs in the Streamlit server process. When deployed remotely,
the uploaded resume is sent to that server; it does not remain on the browser device.
The app does not intentionally write uploaded resumes to disk.
