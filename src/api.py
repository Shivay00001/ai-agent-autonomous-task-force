from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from src.graphs.task_force import create_task_force_graph
from langchain_core.messages import HumanMessage
import uuid

app = FastAPI(title="AI Agent Task Force API")

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    task_id: str
    status: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    task_id = str(uuid.uuid4())
    # In a real system, we would run this in a background worker or stream back response
    return {"task_id": task_id, "status": "initiated"}

@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    return {"task_id": task_id, "state": "processing"}
