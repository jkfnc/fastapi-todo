from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.logging_config import get_logger

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

logger = get_logger("todo_app.database")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

logger.info(f"Database engine created for {SQLALCHEMY_DATABASE_URL}")

def get_db():
    logger.debug("Creating database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing database session")
        db.close()