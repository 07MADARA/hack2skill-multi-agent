from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from agents import run_multi_agent_workflow
import database

# Initialize the db when the API starts
try:
    database.init_db()
except Exception as e:
    print(f"Failed to initialize db: {e}")

app = FastAPI(title="Multi-Agent Hackathon API")

class TaskRequest(BaseModel):
    user_request: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Multi-Agent Hackathon API!", 
        "hint": "Navigate to /docs to use the Swagger UI to test the endpoints."
    }

@app.post("/execute_task")
async def execute_task(request: TaskRequest):
    """
    Endpoint catches the request, hands it to Primary Agent,
    waits for them to finish, and returns the final answer.
    """
    result = run_multi_agent_workflow(request.user_request)
    return {
        "status": "success",
        "original_message": request.user_request,
        "agent_response": result
    }

if __name__ == "__main__":
    print("Starting FastAPI Server... Use: uvicorn main:app --reload")
