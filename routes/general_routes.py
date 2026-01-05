"""
General Routes
==============
Public endpoints like health check and root.
"""

from datetime import datetime
from fastapi import APIRouter

from models import MessageResponse, HealthResponse


router = APIRouter(tags=["General"])


@router.get("/", response_model=MessageResponse)
def root():
    """Root endpoint - Welcome message"""
    return {"message": "Hello World - Welcome to the Auth API!"}


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
