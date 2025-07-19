import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging_config import get_logger

logger = get_logger("todo_app.middleware")

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request details
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Log query parameters if present
        if request.query_params:
            logger.info(f"Query parameters: {dict(request.query_params)}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response details
        logger.info(
            f"Response: {response.status_code} for {request.method} {request.url.path} "
            f"in {process_time:.4f}s"
        )
        
        # Log error responses with more detail
        if response.status_code >= 400:
            logger.error(
                f"Error response: {response.status_code} for {request.method} {request.url.path} "
                f"in {process_time:.4f}s"
            )
        
        return response