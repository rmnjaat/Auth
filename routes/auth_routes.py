"""
Authentication Routes
=====================
Login and token refresh endpoints.
"""

import jwt
from fastapi import APIRouter, HTTPException , Response

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from models import LoginRequest, RefreshTokenRequest, TokenResponse
from database import authenticate_user, get_user_by_username
from auth import create_access_token, create_refresh_token, decode_refresh_token

import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Response, Request
## store session_id , {"user_name": "admin", "role": "admin"}
redis_json = {}

SESSION_TTL  = 30*60 #seconds


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Authenticate user and return access + refresh tokens.
    
    **Demo Credentials:**
    - admin / admin123
    - user1 / password123  
    - test / test123
    """
    # Validate credentials against user database
    user = authenticate_user(request.username, request.password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # Create token payload (NEVER include password!)
    token_data = {
        "username": user["username"],
        "role": user.get("role", "user")
    }
    
    # Generate tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"username": user["username"]})
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest):
    """
    Get a new access token using a valid refresh token.
    
    Use this when your access token expires (401 error).
    """
    try:
        # Decode and validate the refresh token
        payload = decode_refresh_token(request.refresh_token)
        
        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type. Please use a refresh token."
            )
        
        # Extract username
        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )
        
        # Verify user still exists and is active
        user = get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=401,
                detail="User account is disabled"
            )
        
        # Generate new access token with user role
        new_access_token = create_access_token({
            "username": username,
            "role": user.get("role", "user")
        })
        
        return {
            "message": "Token refreshed successfully",
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired. Please login again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )


### Session Managment
# generate session_id
@router.post("/session_log_in")
def session_log_in(request: LoginRequest, response: Response):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    session_id = str(uuid.uuid4())

    redis_json[session_id] = {
        "username": user["username"],
        "role": user.get("role", "user"),
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(minutes=SESSION_TTL)
    }

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=SESSION_TTL
    )

    return {
        "message": "Login successful"
    }



@router.post("/session_log_out")
def session_log_out(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Session ID missing"
        )
    
    if session_id in redis_json:
        del redis_json[session_id]
    
    response.delete_cookie("session_id")
    
    return {"message": "Logout successful"}

@router.post("/rotate_session")
def rotate_session(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Session ID missing"
        )
    
    user = redis_json.get(session_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID"
        )
    
    del redis_json[session_id]

    session_id = str(uuid.uuid4())
    
    redis_json[session_id] = {
        "username": user["username"],
        "role": user.get("role", "user"),
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(minutes=SESSION_TTL)
    }
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=SESSION_TTL
    )
    
    return {"message": "Session rotated successfully"}
  