# FastAPI Todo Application

A simple REST API for managing todos built with FastAPI and SQLAlchemy.

## Features

- Create, read, update, and delete todos
- SQLite database for data persistence
- Automatic API documentation with Swagger UI
- CORS enabled for frontend integration

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

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `GET /` - Welcome message
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
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
└── README.md              # This file
```