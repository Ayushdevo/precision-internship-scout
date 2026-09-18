"""MCP adapter for the local demonstration job source."""
from fastmcp import FastMCP
from jobs import fetch_vetted_jobs as search_jobs

mcp = FastMCP("PrecisionJobScout")

@mcp.tool()
def fetch_vetted_jobs(role_keyword: str) -> list:
    """Search illustrative sample jobs; these are not verified live vacancies."""
    return search_jobs(role_keyword)

if __name__ == "__main__":
    mcp.run()
