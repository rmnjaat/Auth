"""
Pydantic Models
===============
Request and Response models for the API.
"""

from typing import Optional
from pydantic import BaseModel


# ============ REQUEST MODELS ============

class LoginRequest(BaseModel):
    """Login request body"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request body"""
    refresh_token: str


# ============ RESPONSE MODELS ============

class TokenResponse(BaseModel):
    """Token response model"""
    message: str
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
