from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dataclasses import dataclass

app = FastAPI()

tasks = [
    {
        "id" : 1,
        "title" : "Plan your day",
        "done" : False
    },{
        "id": 2,
        "title": "Clean the bathroom",
        "done": False 
    },{
        "id": 3,
        "title": "Go to grocery store",
        "done": True
    }
]

task_count = 3


class CreateTask(BaseModel):
    title: str

@app.get("/")
def home():
    return { 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] 
        }

@app.get("/tasks")
def getTasks():
    return tasks;

@app.get("/tasks/{id}")
def getTaskById(id: int):
    
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.post("/tasks")
def create_task(task: CreateTask):

    if task.title is None or not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid title"}
        )

    global task_count
    task_count += 1

    created_task = {
        "id": task_count,
        "title": task.title,
        "done": False
    }

    tasks.append(created_task)

    return JSONResponse(
        status_code=201,
        content=created_task
    )


@app.get("/health")
def health():
    return {"status": "ok"}

