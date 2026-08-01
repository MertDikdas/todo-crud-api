from fastapi import FastAPI
from fastapi.responses import JSONResponse

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


@app.get("/health")
def health():
    return {"status": "ok"}