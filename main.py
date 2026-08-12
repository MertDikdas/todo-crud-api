from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional
import sqlite3

def get_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

app = FastAPI()

class CreateTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/", summary="Get API information")
def home():
    return { 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] 
        }

@app.get("/tasks", summary="List all tasks")
def get_tasks(done: Optional[bool] = None):
    conn = get_connection()
    if done is None:
        tasks = conn.execute("SELECT * FROM tasks")
    else:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE done = ?",
            (int(done),)
            )

    rows = tasks.fetchall()
    conn.close()


    return [dict(row) for row in rows]

@app.get("/tasks/{id}", summary="Get a task by ID")
def get_task_by_id(id: int):
    conn = get_connection()
    
    task =conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = task.fetchone()

    conn.close()
    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )
    return dict(row);



@app.post("/tasks", summary="Create a new task")
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
        "title": task.title.strip(),
        "done": False
    }

    tasks.append(created_task)

    return JSONResponse(
        status_code=201,
        content=created_task
    )

@app.put("/tasks/{id}", summary="Update an existing task")
def update_task(id : int, update : UpdateTask):
    if update.title is None and update.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid body"}
        )

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
                status_code=200,
                content=task
            )
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}",summary="Delete a task")
def delete_task(id: int):
    for task in tasks:
        if task["id"]==id:
            tasks.remove(task)
            return Response(status_code=204)
    
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.get("/health",summary="Check API health")
def health():
    return {"status": "ok"}

