from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database.database import engine, Base
from app.routers import todos
from app.logging_config import setup_logging, get_logger
from app.middleware.logging_middleware import LoggingMiddleware

# Setup logging
setup_logging()
logger = get_logger("todo_app.main")

Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

app = FastAPI(title="Todo API", version="1.0.0")
logger.info("FastAPI application initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)
logger.info("Logging middleware added")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

@app.get("/")
async def read_root():
    logger.info("Serving root page")
    return FileResponse("templates/index.html")