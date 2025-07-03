from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import sys

# Add the libs/database_utils/src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'libs', 'database_utils', 'src')))
from database_utils.db_connector import get_sqlite_connection

app = FastAPI()

class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False

# In a real application, you'd use a proper ORM like SQLAlchemy with a database.
# For simplicity, we'll use a direct SQLite connection here.
DATABASE_FILE = "./todo.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name
    return conn

# Initialize database
@app.on_event("startup")
async def startup_event():
    conn = get_sqlite_connection(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    conn = get_sqlite_connection(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
                   (task.title, task.description, task.completed))
    conn.commit()
    task.id = cursor.lastrowid
    conn.close()
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    conn = get_sqlite_connection(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    conn = get_sqlite_connection(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(task)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    conn = get_sqlite_connection(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
                   (task.title, task.description, task.completed, task_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.close()
    task.id = task_id # Ensure the ID is set for the response model
    return task

@app.delete("/tasks/{task_id}", response_model=Dict[str, str])
async def delete_task(task_id: int):
    conn = get_sqlite_connection(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.close()
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    print(f"To run the API: uvicorn main:app --reload --port 8000")
    print(f"Access it at http://127.0.0.1:8000/docs")
    # uvicorn.run(app, host="0.0.0.0", port=8000) # Uncomment to run directly
