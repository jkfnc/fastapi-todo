"""Simple test script to verify logging functionality"""
import tempfile
import os
from fastapi.testclient import TestClient
from main import app
from app.logging_config import setup_logging

def test_logging():
    """Test that logging is working properly"""
    print("Testing logging functionality...")
    
    # Setup logging
    setup_logging()
    
    # Create a test client
    client = TestClient(app)
    
    # Test various endpoints to generate logs
    print("1. Testing root endpoint...")
    response = client.get("/")
    assert response.status_code == 200
    print("✓ Root endpoint working")
    
    print("2. Testing create todo...")
    todo_data = {
        "title": "Test Logging Todo",
        "description": "Testing logging functionality",
        "completed": False
    }
    response = client.post("/api/todos/", json=todo_data)
    assert response.status_code == 200
    todo_id = response.json()["id"]
    print("✓ Create todo working")
    
    print("3. Testing get all todos...")
    response = client.get("/api/todos/")
    assert response.status_code == 200
    print("✓ Get all todos working")
    
    print("4. Testing get todo by id...")
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    print("✓ Get todo by id working")
    
    print("5. Testing update todo...")
    update_data = {"title": "Updated Test Todo", "completed": True}
    response = client.put(f"/api/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    print("✓ Update todo working")
    
    print("6. Testing delete todo...")
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    print("✓ Delete todo working")
    
    print("7. Testing 404 error...")
    response = client.get("/api/todos/9999")
    assert response.status_code == 404
    print("✓ 404 error handling working")
    
    print("\n✅ All logging tests passed!")
    print("📋 Check the logs/todo_app.log file for detailed logging output")
    
    # Check if log file was created
    if os.path.exists("logs/todo_app.log"):
        print("📄 Log file created successfully")
        with open("logs/todo_app.log", "r") as f:
            log_content = f.read()
            if log_content:
                print("📝 Log file contains content")
                print(f"📊 Log file size: {len(log_content)} characters")
            else:
                print("⚠️ Log file is empty")
    else:
        print("❌ Log file not found")

if __name__ == "__main__":
    test_logging()