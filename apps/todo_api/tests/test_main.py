# apps/todo_api/tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from todo_api.main import app
from todo_api.database import get_db, TABLE_NAME, TABLE_SCHEMA
import sqlite3
import os

@pytest.fixture(scope="function")
def client(tmp_path_factory, monkeypatch):
    db_path = tmp_path_factory.mktemp("data") / "test_todo.db"
    
    def override_get_db():
        from database_utils.db_connector import DatabaseManager
        return DatabaseManager(db_path)

    monkeypatch.setattr("todo_api.main.get_db", override_get_db)
    
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        conn.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({TABLE_SCHEMA})")
        conn.commit()
        
    yield TestClient(app)


def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

def test_read_tasks(client):
    client.post("/tasks/", json={"title": "Test Task 1", "description": "Test Description 1"})
    client.post("/tasks/", json={"title": "Test Task 2", "description": "Test Description 2"})
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_read_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"

def test_update_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated Description", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] is True

def test_delete_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404