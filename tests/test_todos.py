import pytest
from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Todo API"}

def test_create_todo(client: TestClient):
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    }
    response = client.post("/api/todos/", json=todo_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data
    assert "created_at" in data

def test_get_todos(client: TestClient):
    # Create a todo first
    todo_data = {"title": "Test Todo", "description": "Test", "completed": False}
    client.post("/api/todos/", json=todo_data)
    
    response = client.get("/api/todos/")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) == 1
    assert todos[0]["title"] == "Test Todo"

def test_get_todo_by_id(client: TestClient):
    # Create a todo
    todo_data = {"title": "Test Todo", "description": "Test", "completed": False}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Get the todo by ID
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"

def test_get_todo_not_found(client: TestClient):
    response = client.get("/api/todos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_update_todo(client: TestClient):
    # Create a todo
    todo_data = {"title": "Original Title", "description": "Original", "completed": False}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Update the todo
    update_data = {"title": "Updated Title", "completed": True}
    response = client.put(f"/api/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] == True
    assert data["description"] == "Original"  # Should remain unchanged

def test_update_todo_not_found(client: TestClient):
    update_data = {"title": "Updated Title"}
    response = client.put("/api/todos/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_delete_todo(client: TestClient):
    # Create a todo
    todo_data = {"title": "To Delete", "description": "Test", "completed": False}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Delete the todo
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404

def test_delete_todo_not_found(client: TestClient):
    response = client.delete("/api/todos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"