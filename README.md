# FastAPI Todo Application

A full-stack todo application with a REST API backend and interactive web frontend, built with FastAPI and SQLAlchemy.

## Features

- **Backend**: RESTful API with FastAPI
  - Create, read, update, and delete todos
  - SQLite database for data persistence
  - Automatic API documentation with Swagger UI
  - CORS enabled for frontend integration
  
- **Frontend**: Modern web interface
  - Responsive design that works on desktop and mobile
  - Real-time todo management without page refresh
  - Filter todos by status (All, Active, Completed)
  - Clean, intuitive user interface

## Installation

1. Clone the repository:
```bash
cd fastapi-todo
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Accessing the Application

- **Web Frontend**: `http://localhost:8000`
- **API Documentation**: 
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `GET /` - Serves the web frontend
- `GET /api/todos` - Get all todos
- `GET /api/todos/{todo_id}` - Get a specific todo
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{todo_id}` - Update a todo
- `DELETE /api/todos/{todo_id}` - Delete a todo

## Project Structure

```
fastapi-todo/
├── app/
│   ├── database/
│   │   └── database.py     # Database configuration
│   ├── models/
│   │   └── todo.py         # SQLAlchemy models
│   ├── routers/
│   │   └── todos.py        # API routes
│   └── schemas/
│       └── todo.py         # Pydantic schemas
├── static/
│   ├── css/
│   │   └── style.css       # Frontend styles
│   └── js/
│       └── app.js          # Frontend JavaScript
├── templates/
│   └── index.html          # Frontend HTML
├── tests/
│   ├── test_todos.py       # API tests
│   ├── test_frontend.py    # Frontend integration tests
│   └── test_frontend_js.py # JavaScript functionality tests
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Running Tests

```bash
pytest tests/ -v
```