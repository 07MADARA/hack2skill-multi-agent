# Multi-Agent AI System - Task & Schedule Manager 🤖

**Submission for Hack2Skill Hackathon (Track 3)**

This project is a multi-agent AI system designed to help users manage tasks, schedules, and information by interacting with multiple tools and data sources. It is deployed as a fully functional API using FastAPI.

## 🌟 Live Demo & Links
* **Live API URL:** [Insert your Render URL here, e.g., https://my-agent.onrender.com/docs]
* **Demo Video:** [Insert link to your YouTube/Drive demo video here]

## 🎯 Core Requirements Met
1. **Primary Agent Coordination:** A Primary Orchestrator agent receives user prompts and routes them to the appropriate sub-agents.
2. **Sub-Agents:** Features specialized sub-agents (Database Manager and Calendar Manager) to execute distinct workflows.
3. **Structured Database:** Integrates an SQLite database (`hackathon.db`) to store, retrieve, and track generated tasks.
4. **Tool Integration (MCP-style):** Agents are equipped with specific functional tools to mock external interactions (e.g., calendar scheduling).
5. **API-Based Deployment:** The entire system is wrapped in a FastAPI application, allowing external platforms to trigger multi-step workflows via standard HTTP POST requests.

## 🛠️ Tech Stack
* **Language:** Python 3
* **API Framework:** FastAPI & Uvicorn
* **Database:** SQLite
* **Agent Logic:** Custom LLM routing logic / Pydantic

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```
   *(Requirements included: `fastapi`, `uvicorn`, `pydantic`, `requests`)*

3. **Set up Environment Variables (Optional):**
   The application uses OpenAI's API to power the primary agent router. If an API key is not provided, it falls back to a mock agent behavior for testing.
   ```powershell
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   ```
   ```bash
   # On Linux/macOS
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Start the API server:**
   Run the application using Uvicorn from the project directory:
   ```bash
   uvicorn main:app --reload
   ```

5. **Test the API:** Open your browser and navigate to `http://127.0.0.1:8000/docs` to use the built-in Swagger UI.

## 📡 API Endpoints

### `POST /execute_task`
This is the primary endpoint to interact with the multi-agent system.

**Request Body (JSON):**
```json
{
  "user_request": "Schedule a hackathon review meeting for tomorrow, and save a task to submit the project files."
}
```

**Expected Response (JSON):**
```json
{
  "status": "success",
  "original_message": "Schedule a hackathon review meeting for tomorrow, and save a task to submit the project files.",
  "agent_response": "Success: Saved 'Demo Video' to database. | Success: Scheduled event 'Hackathon Review'."
}
```

## 🏗️ System Architecture
1. **User Request** -> Sent via POST to `/execute_task`.
2. **Primary Agent (Router)** -> Analyzes the intent of the prompt.
3. **Delegation** -> Routes to:
   - **Database Sub-Agent:** Extracts task data and writes it to SQLite.
   - **Calendar Sub-Agent:** Extracts event data and processes the schedule.
4. **Response Aggregation** -> The primary agent combines the tools' outputs and returns a final success confirmation to the user.
