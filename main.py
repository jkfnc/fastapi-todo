from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo API"}