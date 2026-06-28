import os
from dotenv import load_dotenv

# Load environment variables if needed (.env file support)
load_dotenv()

# Clean handling of fastmcp import for compatibility in environments where python < 3.10 
# or fastmcp is not yet installed.
try:
    from fastmcp import FastMCP
except ImportError:
    # Fallback mock class to prevent execution failure while preserving the correct fastmcp API structure
    class FastMCP:
        def __init__(self, name: str):
            self.name = name
            
        def tool(self):
            # A decorator that returns the function unchanged
            def decorator(func):
                return func
            return decorator
            
        def run(self):
            print(f"[Mock Server] MCP Server '{self.name}' running in compatibility fallback mode.")

# Initialize the FastMCP server named "PrecisionJobScout"
# This server serves as our high-signal data source, bypassing general public recruitment aggregators.
mcp = FastMCP("PrecisionJobScout")

@mcp.tool()
def fetch_vetted_jobs(role_keyword: str) -> list:
    """
    Fetch premium, vetted tech job listings for 2026 AI Engineering Internships.
    This tool serves as an interface for the Scout Agent to programmatically access
    our secure and verified company job pipelines.
    
    Args:
        role_keyword (str): The keyword used to filter relevant internships (e.g., 'AI', 'Quant', 'Research').
        
    Returns:
        list: A list of dict items containing premium, mock tech listings with structured attributes.
    """
    # Curated premium mock listings representing high-signal target pipelines
    mock_jobs = [
        {
            "title": "Research Intern, AI Engineering (2026)",
            "company": "Google DeepMind",
            "location": "London, UK / Mountain View, CA",
            "requirements": [
                "Python",
                "PyTorch",
                "JAX",
                "Transformers",
                "Strong mathematical foundation",
                "Publication record or contribution to open-source AI projects"
            ],
            "target_link": "https://deepmind.google/careers"
        },
        {
            "title": "Quantitative AI Research Intern (2026)",
            "company": "QuantLabs",
            "location": "New York, NY",
            "requirements": [
                "Python",
                "C++",
                "PyTorch",
                "Time-series forecasting",
                "High-performance computing",
                "Stochastic calculus"
            ],
            "target_link": "https://quantlabs.com/careers"
        },
        {
            "title": "AI Platform Engineer Intern (2026)",
            "company": "TechScale AI",
            "location": "San Francisco, CA",
            "requirements": [
                "Python",
                "Docker",
                "vLLM",
                "RAG",
                "LangChain",
                "Vector Databases",
                "API design and microservices"
            ],
            "target_link": "https://techscale.ai/careers"
        }
    ]
    
    # Filter based on search criteria
    if not role_keyword or role_keyword.strip() == "":
        return mock_jobs
        
    keyword_lower = role_keyword.lower()
    filtered_jobs = []
    
    for job in mock_jobs:
        # Check if the keyword matches the title, company, or any of the requirements
        if (keyword_lower in job["title"].lower() or 
            keyword_lower in job["company"].lower() or 
            any(keyword_lower in req.lower() for req in job["requirements"])):
            filtered_jobs.append(job)
            
    # Fallback to returning all jobs if filtering is overly restrictive
    return filtered_jobs if filtered_jobs else mock_jobs

if __name__ == "__main__":
    # Start the FastMCP server when executed directly
    mcp.run()
