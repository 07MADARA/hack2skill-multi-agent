import sqlite3
import json
import requests
import os

# --- DATABASE SETUP (Remains the same) ---
def init_db():
    conn = sqlite3.connect('hackathon.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- THE TOOLS ---
def db_tool(task_name: str) -> str:
    """Saves a new task to the structured SQLite database."""
    conn = sqlite3.connect('hackathon.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name, status) VALUES (?, ?)", (task_name, "pending"))
    conn.commit()
    conn.close()
    return f"Success: Saved '{task_name}' to database."

def calendar_tool(event_details: str) -> str:
    """Mocks scheduling an event."""
    return f"Success: Scheduled event '{event_details}'."

# --- OPTION 2: CUSTOM AGENT LOGIC ---
def call_llm(prompt: str) -> str:
    """A simple function to call an LLM (like OpenAI) using raw requests."""
    api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    # If you don't have an API key yet, we will mock the AI's brain for testing
    if api_key == "your-api-key-here":
        return mock_agent_brain(prompt)

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

def mock_agent_brain(prompt: str) -> str:
    """A temporary mock brain so you can test the API without an API key right now."""
    prompt_lower = prompt.lower()
    if "schedule" in prompt_lower and "save" in prompt_lower:
        return '{"action": "both", "task": "Demo Video", "event": "Hackathon Review"}'
    return '{"action": "unknown"}'

def run_multi_agent_workflow(user_prompt: str):
    """The Primary Agent (Router) that delegates to sub-agents."""
    
    # 1. Primary Agent Routing Phase
    routing_prompt = f"""
    You are the Primary Manager Agent. Analyze this request: "{user_prompt}"
    Determine if you need to use the 'calendar_tool', the 'db_tool', or both.
    Reply ONLY in JSON format: {{"action": "db", "task": "task name"}} or {{"action": "calendar", "event": "event info"}} or {{"action": "both", "task": "task name", "event": "event info"}}
    """
    
    decision_json = call_llm(routing_prompt)
    
    try:
        decision = json.loads(decision_json)
    except:
        return "Error: Primary agent failed to format instructions."

    results = []

    # 2. Sub-Agent Execution Phase
    if decision.get("action") in ["db", "both"]:
        # Hand off to Database Sub-Agent
        results.append(db_tool(decision.get("task", "Unknown Task")))
        
    if decision.get("action") in ["calendar", "both"]:
        # Hand off to Calendar Sub-Agent
        results.append(calendar_tool(decision.get("event", "Unknown Event")))

    return " | ".join(results)
