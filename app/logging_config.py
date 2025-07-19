import logging
import logging.config
import os
from typing import Dict, Any

def setup_logging() -> None:
    """Configure logging for the FastAPI todo application."""
    
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "level": log_level,
                "filename": "logs/todo_app.log",
                "mode": "a",
                "encoding": "utf-8"
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console", "file"]
        },
        "loggers": {
            "todo_app": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "fastapi": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            }
        }
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logging.config.dictConfig(logging_config)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)