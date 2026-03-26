from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse  # <-- This is the new tool we imported
from pydantic import BaseModel
from agents import run_multi_agent_workflow

# Initialize the API
app = FastAPI(title="Multi-Agent Task System", description="API for Hack2Skill Submission")

# Define what the incoming data should look like
class PromptRequest(BaseModel):
    user_request: str

# Create the Endpoint
@app.post("/execute_task")
async def execute_task(request: PromptRequest):
    try:
        # Pass the user's prompt into the custom workflow
        agent_response = run_multi_agent_workflow(request.user_request)
        
        # Return the final result
        return {
            "status": "success", 
            "original_message": request.user_request,
            "agent_response": str(agent_response)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- THE MAGIC REDIRECT ---
@app.get("/")
async def root():
    # This instantly teleports anyone who visits the base link directly to the /docs page!
    return RedirectResponse(url="/docs")
