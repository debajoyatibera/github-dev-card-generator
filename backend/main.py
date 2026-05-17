from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from adk.agents import generate_dev_card

app = FastAPI(title="GitHub Dev Card Generator API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DevCardRequest(BaseModel):
    username: str

class DevCardResponse(BaseModel):
    username: str
    name: str = None
    bio: str = None
    followers: int = 0
    following: int = 0
    public_repos: int = 0
    top_languages: list[str] = []
    summary: str = ""
    card_style: str = ""

@app.post("/generate", response_model=DevCardResponse)
async def generate(request: DevCardRequest):
    try:
        raw_result = await generate_dev_card(request.username)
        
        # Parse the JSON from the agent response
        # The agent might return markdown-wrapped JSON, so we should clean it
        clean_result = raw_result.strip()
        if clean_result.startswith("```json"):
            clean_result = clean_result[7:-3].strip()
        elif clean_result.startswith("```"):
            clean_result = clean_result[3:-3].strip()
            
        data = json.loads(clean_result)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
