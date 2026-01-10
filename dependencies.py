"""
FastAPI Dependencies
====================
Reusable dependencies for route protection.
"""

import jwt
from fastapi import Request, HTTPException

from config import SECRET_KEY, ALGORITHM
from database import get_user_by_username

from datetime import datetime
from routes.auth_routes import redis_json

def authorize_user(request: Request) -> str:
    """
    Validate access token from Authorization header.
    
    Used as a Security dependency for protected routes.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Username from the valid token
        
    Raises:
        HTTPException: 401 for invalid/missing/expired tokens
    """
    auth_header = request.headers.get("Authorization")
    
    # Step 1: Check if Authorization header exists
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    # Step 2: Extract token from "Bearer <token>" format
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid auth header format. Use: Bearer <token>"
        )
    
    token = parts[1]
    
    # Step 3: Decode and validate the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Step 4: Verify token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type. Use access token."
            )
        
        # Step 5: Extract and validate username
        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )
        
        # Step 6: Verify user still exists and is active
        user = get_user_by_username(username)
        if not user or not user.get("is_active", True):
            raise HTTPException(
                status_code=401,
                detail="User account is disabled or not found"
            )
        
        return username
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def authorize_session(request: Request) -> str:
    """
    Validate session from cookie.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Username from the valid session
        
    Raises:
        HTTPException: 401 for invalid/missing/expired session
    """
    # Get session_id from cookies (FastAPI handles cookie parsing)
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Session ID missing"
        )
    
    # Validate session exists
    session_data = redis_json.get(session_id)
    if not session_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID"
        )
    
    # Check if session expired
    if session_data.get("expires_at") < datetime.now():
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )
    
    return session_data.get("username")
