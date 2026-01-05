"""
FastAPI Authentication API
==========================
Main application entry point.

Project Structure:
├── main.py           # This file - App initialization
├── config.py         # Configuration settings
├── database.py       # Dummy user database
├── models.py         # Pydantic models
├── auth.py           # JWT token utilities
├── dependencies.py   # FastAPI dependencies
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py    # Login, refresh endpoints
│   └── general_routes.py # Root, health endpoints
├── m1/               # Protected module
└── m2/               # Public module
"""

from fastapi import FastAPI, Security
import uvicorn

# Import dependencies
from dependencies import authorize_user

# Import routers
from routes.auth_routes import router as auth_router
from routes.general_routes import router as general_router
from m1 import mf1 as m1_router
from m2 import mf2 as m2_router


# ============ APP INITIALIZATION ============

app = FastAPI(
    title="Auth Learning API",
    description="JWT Authentication with Access & Refresh Tokens",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ============ REGISTER ROUTERS ============

# General routes (public)
app.include_router(general_router)

# Auth routes (public - login/refresh)
app.include_router(auth_router)

# m1 routes - PROTECTED (require auth)
app.include_router(
    m1_router.router,
    dependencies=[Security(authorize_user)]
)

# m2 routes - PUBLIC (no auth required)
app.include_router(m2_router.router)


# ============ ENTRYPOINT ============

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
