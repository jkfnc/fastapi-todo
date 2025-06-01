import pytest
from fastapi.testclient import TestClient
import json

def test_frontend_creates_todo_via_api(client: TestClient):
    """Test that the frontend JavaScript can create todos via API"""
    # Simulate what the frontend JavaScript does
    headers = {"Content-Type": "application/json"}
    todo_data = {
        "title": "JavaScript Created Todo",
        "description": "Created by simulating frontend JS",
        "completed": False
    }
    
    response = client.post("/api/todos/", json=todo_data, headers=headers)
    assert response.status_code == 200
    
    created_todo = response.json()
    assert created_todo["title"] == todo_data["title"]
    assert created_todo["description"] == todo_data["description"]
    assert created_todo["completed"] == todo_data["completed"]
    assert "id" in created_todo
    assert "created_at" in created_todo

def test_frontend_updates_todo_via_api(client: TestClient):
    """Test that the frontend JavaScript can update todos via API"""
    # Create a todo first
    todo_data = {"title": "To Be Updated", "description": "Original", "completed": False}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Update it like the frontend would
    update_data = {"completed": True}
    update_response = client.put(f"/api/todos/{todo_id}", json=update_data)
    assert update_response.status_code == 200
    
    updated_todo = update_response.json()
    assert updated_todo["completed"] == True
    assert updated_todo["title"] == "To Be Updated"

def test_frontend_deletes_todo_via_api(client: TestClient):
    """Test that the frontend JavaScript can delete todos via API"""
    # Create a todo first
    todo_data = {"title": "To Be Deleted", "description": "Test", "completed": False}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Delete it like the frontend would
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404

def test_frontend_filters_todos(client: TestClient):
    """Test the todo filtering logic that frontend would use"""
    # Create multiple todos with different states
    todos = [
        {"title": "Active Todo 1", "description": "Not done", "completed": False},
        {"title": "Completed Todo 1", "description": "Done", "completed": True},
        {"title": "Active Todo 2", "description": "Not done", "completed": False},
    ]
    
    created_ids = []
    for todo in todos:
        response = client.post("/api/todos/", json=todo)
        created_ids.append(response.json()["id"])
    
    # Get all todos
    response = client.get("/api/todos/")
    all_todos = response.json()
    
    # Simulate frontend filtering
    active_todos = [t for t in all_todos if not t["completed"]]
    completed_todos = [t for t in all_todos if t["completed"]]
    
    assert len(active_todos) >= 2
    assert len(completed_todos) >= 1