from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.todo import Todo
from app.schemas.todo import Todo as TodoSchema, TodoCreate, TodoUpdate
from app.logging_config import get_logger

router = APIRouter()
logger = get_logger("todo_app.routers.todos")

@router.get("/", response_model=List[TodoSchema])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Fetching todos with skip={skip}, limit={limit}")
    todos = db.query(Todo).offset(skip).limit(limit).all()
    logger.info(f"Found {len(todos)} todos")
    return todos

@router.get("/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching todo with id={todo_id}")
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        logger.warning(f"Todo with id={todo_id} not found")
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info(f"Found todo: {todo.title}")
    return todo

@router.post("/", response_model=TodoSchema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new todo: {todo.title}")
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    logger.info(f"Created todo with id={db_todo.id}: {db_todo.title}")
    return db_todo

@router.put("/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating todo with id={todo_id}")
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        logger.warning(f"Todo with id={todo_id} not found for update")
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_data = todo.model_dump(exclude_unset=True)
    logger.info(f"Updating todo {todo_id} with data: {todo_data}")
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    logger.info(f"Updated todo {todo_id}: {db_todo.title}")
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting todo with id={todo_id}")
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        logger.warning(f"Todo with id={todo_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_title = db_todo.title
    db.delete(db_todo)
    db.commit()
    logger.info(f"Deleted todo {todo_id}: {todo_title}")
    return {"message": "Todo deleted successfully"}