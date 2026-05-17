from fastmcp import FastMCP
import httpx
import os

mcp = FastMCP("GitHubTool")

GITHUB_API_URL = "https://api.github.com"

@mcp.tool()
async def get_github_user(username: str):
    """Fetch GitHub profile information for a given username."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_URL}/users/{username}")
        if response.status_code != 200:
            return {"error": f"User {username} not found or API error."}
        return response.json()

@mcp.tool()
async def get_github_repos(username: str):
    """Fetch list of public repositories for a given GitHub username."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_URL}/users/{username}/repos?sort=updated&per_page=10")
        if response.status_code != 200:
            return {"error": f"Could not fetch repos for {username}."}
        return response.json()

if __name__ == "__main__":
    mcp.run()
