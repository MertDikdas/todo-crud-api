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

    conn = get_connection()

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title.strip(), 0)
    )

    conn.commit()

    created_id = cursor.lastrowid

    cursor = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (created_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return JSONResponse(
        status_code=201,
        content=dict(row)
    )

@app.put("/tasks/{id}", summary="Update an existing task")
def update_task(id: int, update: UpdateTask):

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

    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )


    current_title = row["title"]
    current_done = row["done"]

    new_title = (
        update.title.strip()
        if update.title is not None
        else current_title
    )

    new_done = (
        int(update.done)
        if update.done is not None
        else current_done
    )


    conn.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (new_title, new_done, id)
    )

    conn.commit()

    cursor = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    updated_row = cursor.fetchone()

    conn.close()

    return JSONResponse(
        status_code=200,
        content=dict(updated_row)
    )

@app.delete("/tasks/{id}", summary="Delete a task")
def delete_task(id: int):

    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return Response(status_code=204)


@app.get("/health",summary="Check API health")
def health():
    return {"status": "ok"}

