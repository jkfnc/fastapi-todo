import pytest
from fastapi.testclient import TestClient

def test_home_page_loads(client: TestClient):
    """Test that the home page loads successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>Todo App</title>" in response.text
    assert '<h1>My Todo List</h1>' in response.text

def test_static_css_loads(client: TestClient):
    """Test that CSS file is served correctly"""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    assert "--primary-color" in response.text

def test_static_js_loads(client: TestClient):
    """Test that JavaScript file is served correctly"""
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]
    assert "TodoApp" in response.text

def test_frontend_api_integration(client: TestClient):
    """Test that frontend can interact with API"""
    # Create a todo via API
    todo_data = {"title": "Frontend Test Todo", "description": "Test", "completed": False}
    create_response = client.post("/api/todos/", json=todo_data)
    assert create_response.status_code == 200
    
    # Verify the home page still loads
    response = client.get("/")
    assert response.status_code == 200
    
    # Verify API endpoint is accessible
    api_response = client.get("/api/todos/")
    assert api_response.status_code == 200
    todos = api_response.json()
    assert len(todos) > 0
    assert todos[0]["title"] == "Frontend Test Todo"