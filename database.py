"""
Dummy User Database
===================
Simulated user database for authentication.
In production, replace with actual database (PostgreSQL, MongoDB, etc.)
"""

from typing import Optional


# Simulated user database (list of user dictionaries)
# NOTE: In real app, use hashed passwords with bcrypt/argon2!
USERS_DB = [
    {
        "id": 1,
        "username": "admin",
        "password": "admin123",     # Plain text for demo ONLY!
        "email": "admin@example.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "username": "user1",
        "password": "password123",
        "email": "user1@example.com",
        "role": "user",
        "is_active": True
    },
    {
        "id": 3,
        "username": "test",
        "password": "test123",
        "email": "test@example.com",
        "role": "user",
        "is_active": True
    },
    {
        "id": 4,
        "username": "inactive_user",
        "password": "inactive123",
        "email": "inactive@example.com",
        "role": "user",
        "is_active": False  # This user is disabled
    }
]


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Validate user credentials against the database.
    
    Args:
        username: The username to validate
        password: The plain-text password to check
        
    Returns:
        User dict if valid, None otherwise
        
    Note:
        In production, use password hashing (bcrypt/argon2) like:
        - Store: hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        - Verify: bcrypt.checkpw(password, hashed_password)
    """
    for user in USERS_DB:
        if user["username"] == username and user["password"] == password:
            # Check if user account is active
            if not user.get("is_active", True):
                return None  # Account is disabled
            return user
    return None


def get_user_by_username(username: str) -> Optional[dict]:
    """
    Retrieve user by username.
    
    Args:
        username: The username to look up
        
    Returns:
        User dict if found, None otherwise
    """
    for user in USERS_DB:
        if user["username"] == username:
            return user
    return None
