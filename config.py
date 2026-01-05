"""
Configuration settings for the Auth API
=======================================
All configuration constants and settings go here.
In production, load these from environment variables!
"""

# JWT Settings
SECRET_KEY = "secret"                      # TODO: Use env variable in production!
REFRESH_SECRET_KEY = "refresh_secret"      # Separate secret for refresh tokens
ALGORITHM = "HS256"

# Token Expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 15           # Access token TTL: 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7              # Refresh token TTL: 7 days
