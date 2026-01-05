from fastapi import FastAPI, HTTPException , Security , Request
import uvicorn
import jwt
from datetime import datetime, timedelta


from m1 import mf1 as m1_router  
from m2 import mf2 as m2_router

from pydantic import BaseModel

# ============ CONFIGURATION ============
SECRET_KEY = "secret"                    # Use a strong secret in production!
REFRESH_SECRET_KEY = "refresh_secret"    # Different secret for refresh tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 15         # Access token TTL: 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7            # Refresh token TTL: 7 days
ALGORITHM = "HS256"

# ============ MODELS ============
class Login(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

### verify token
def authorize_user(request: Request):
    auth_header = request.headers.get("Authorization")
    
    # Step 1: Check if Authorization header exists
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Step 2: Extract token from "Bearer <token>" format FIRST!
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth header format. Use: Bearer <token>")
    
    token = parts[1]  # This is the actual JWT token
    
    # Step 3: NOW decode the extracted token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Step 4: Check token type (should be access token, not refresh)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type. Use access token.")
        
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
            
        return username
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============ TOKEN FUNCTIONS ============
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create an access token with expiration"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,           # Expiration time
        "iat": datetime.utcnow(), # Issued at time
        "type": "access"         # Token type
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    """Create a refresh token with longer expiration"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"        # Token type
    })
    
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


# ============ APP SETUP ============
app = FastAPI(
    title="My Learning API",
    description="Learning FastAPI Routers",
    version="1.0.0"
)

# Register the routers with the main app
app.include_router(m1_router.router , 
dependencies=[Security(authorize_user)])
app.include_router(m2_router.router)

# ============ ROUTES ============

# Root route
@app.get("/")
def root():
    return {"message": "Hello World - Welcome to the API!"}

# Health check route
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Login API - Returns both access and refresh tokens
@app.post("/login")
def login(request: Login):
    # In real app, validate username/password against database here!
    
    # Create token payload (DON'T include password in token!)
    token_data = {"username": request.username}
    
    # Generate tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {

        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    }


# Refresh Token API - Get new access token using refresh token
@app.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    try:
        # Decode and validate the refresh token
        payload = jwt.decode(
            request.refresh_token, 
            REFRESH_SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        
        # Check if it's actually a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401, 
                detail="Invalid token type. Please use a refresh token."
            )
        
        # Extract username from refresh token
        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=401, 
                detail="Invalid token payload"
            )
        
        # Generate new access token
        new_access_token = create_access_token({"username": username})
        
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
