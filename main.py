from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional

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

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

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

@app.put("/tasks/{id}")
def updateTask(id : int, update : UpdateTask):
    if update.title is not None and not update.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid title"}
        )
    
    for task in tasks:
        if task["id"] == id:
            if update.title is not None and update.title.strip():
                task["title"] = update.title.strip()
            if update.done is not None:
                task["done"] = update.done
            return JSONResponse(
                status_code=201,
                content=task
            )
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}")
def deleteTask(id: int):
    for task in tasks:
        if task["id"]==id:
            tasks.remove(task)
            return Response(status_code=204)
    
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.get("/health")
def health():
    return {"status": "ok"}

