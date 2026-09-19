def fetch_vetted_jobs(role_keyword: str) -> list:
    """Search illustrative sample listings, not verified current openings.

    Empty keywords return all samples; unmatched keywords return an empty list.
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
    
    for job in mock_jobs:
        job["source_type"] = "demo"
        job["verified"] = False
    # Filter based on search criteria
    if not role_keyword or role_keyword.strip() == "":
        return mock_jobs
        
    keyword_lower = role_keyword.strip().casefold()
    filtered_jobs = []
    
    for job in mock_jobs:
        # Check if the keyword matches the title, company, or any of the requirements
        if (keyword_lower in job["title"].lower() or 
            keyword_lower in job["company"].lower() or
            keyword_lower in job["location"].casefold() or
            any(keyword_lower in req.lower() for req in job["requirements"])):
            filtered_jobs.append(job)
            
    # An empty match set is a valid search result.
    return filtered_jobs
