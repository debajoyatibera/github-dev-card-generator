from google.adk.agents import Agent
from google.adk.tools import McpToolset
import os
import sys

# Define the path to the MCP server
# We'll use the absolute path to ensure it works regardless of where the script is run
MCP_SERVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mcp", "tools.py"))

def get_dev_card_agent():
    # Connect to the MCP server
    mcp_tools = McpToolset.from_server(
        command=sys.executable,
        args=[MCP_SERVER_PATH]
    )

    # Define the Dev Card Generator Agent
    agent = Agent(
        name="GitHubDevCardGenerator",
        model="gemini-2.0-flash", # Using 2.0 as 2.5 might not be widely available yet
        instructions="""
        You are an expert at creating GitHub Dev Cards. 
        Your goal is to summarize a user's GitHub profile and top repositories into a concise, 
        visually appealing, and informative summary.
        
        Steps:
        1. Fetch the user's profile information using 'get_github_user'.
        2. Fetch the user's top repositories using 'get_github_repos'.
        3. Synthesize this data into a JSON object with the following fields:
           - username
           - name
           - bio
           - followers
           - following
           - public_repos
           - top_languages (infer from repo descriptions and names)
           - summary (a 2-sentence professional summary)
           - card_style (suggest a color theme based on their bio/activity)
        
        Return ONLY the JSON object.
        """,
        tools=[mcp_tools]
    )
    
    return agent

async def generate_dev_card(username: str):
    agent = get_dev_card_agent()
    response = await agent.run(f"Generate a dev card for the GitHub user: {username}")
    return response.content
