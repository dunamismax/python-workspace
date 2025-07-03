# apps/todo_api/src/todo_api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from .database import get_db

app = FastAPI(
    title="To-Do List API",
    description="A simple and efficient API for managing your to-do lists.",
    version="1.0.0",
)

class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False

@app.post("/tasks/", response_model=Task, status_code=201)
async def create_task(task: Task):
    """Creates a new task in the database."""
    query = "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)"
    with get_db() as db:
        cursor = db.execute_query(query, (task.title, task.description, task.completed))
        task.id = cursor.lastrowid
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    """Retrieves all tasks from the database."""
    query = "SELECT * FROM tasks"
    with get_db() as db:
        tasks = db.fetchall(query)
    return [dict(row) for row in tasks]

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    """Retrieves a single task by its ID."""
    query = "SELECT * FROM tasks WHERE id = ?"
    with get_db() as db:
        task = db.fetchone(query, (task_id,))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(task)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    """Updates an existing task."""
    query = "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?"
    with get_db() as db:
        cursor = db.execute_query(query, (task.title, task.description, task.completed, task_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    task.id = task_id
    return task

@app.delete("/tasks/{task_id}", response_model=Dict[str, str])
async def delete_task(task_id: int):
    """Deletes a task from the database."""
    query = "DELETE FROM tasks WHERE id = ?"
    with get_db() as db:
        cursor = db.execute_query(query, (task_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    from .database import initialize_database
    initialize_database()
    print("To run the API, use the command:")
    print("uvicorn todo_api.main:app --reload --port 8000")
    print("Access the API documentation at http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)