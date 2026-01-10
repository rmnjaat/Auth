# 🔐 Auth API - Learning Project

A **FastAPI-based authentication system** implementing both **JWT tokens** and **session-based authentication** for learning purposes.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Authentication Methods](#-authentication-methods)
- [Usage Examples](#-usage-examples)
- [Configuration](#️-configuration)
- [Demo Credentials](#-demo-credentials)

---

## ✨ Features

### Implemented ✅

**JWT-Based Authentication:**
- Access & Refresh Tokens with different expiration times
- Bearer token authentication for protected routes
- Token refresh mechanism
- User role support in token payload

**Session-Based Authentication:**
- Cookie-based session management
- Session login/logout functionality
- Session rotation for enhanced security
- In-memory session storage (Redis-like dictionary)

**Architecture:**
- Modular code organization
- Protected and public route modules
- FastAPI security dependencies
- Comprehensive API documentation

---

## 📁 Project Structure

```
Auth/
├── main.py              # 🚀 App entry point
├── config.py            # ⚙️ Configuration settings
├── database.py          # 🗄️ User database & auth helpers
├── models.py            # 📦 Pydantic models
├── auth.py              # 🔐 JWT token utilities
├── dependencies.py      # 🛡️ Security dependencies (JWT & Session)
├── routes/
│   ├── auth_routes.py   # 🔑 Login, refresh & session endpoints
│   └── general_routes.py# 🏠 Health & root endpoints
├── m1/                  # 🔒 JWT-protected module
├── m2/                  # 🌐 Public module
└── m3/                  # 🍪 Session-protected module
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Auth

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pyjwt

# Run the server
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

📚 **API Docs**: `http://localhost:8000/docs`

---

## 🔗 API Endpoints

### General Routes
| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/` | ❌ | Welcome message |
| `GET` | `/health` | ❌ | Health check |

### JWT Authentication Routes
| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `POST` | `/auth/login` | ❌ | Login & get JWT tokens |
| `POST` | `/auth/refresh` | ❌ | Refresh access token |
| `*` | `/m1/*` | ✅ JWT | JWT-protected routes |

### Session Authentication Routes
| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `POST` | `/auth/session_log_in` | ❌ | Login & get session cookie |
| `POST` | `/auth/session_log_out` | 🍪 | Logout & clear session |
| `POST` | `/auth/rotate_session` | 🍪 | Rotate session ID |
| `*` | `/m3/*` | ✅ Session | Session-protected routes |

### Public Routes
| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `*` | `/m2/*` | ❌ | Public routes (no auth) |

---

## 🔄 Authentication Methods

### 1. JWT-Based Authentication

**Flow:**
```
1. Login → Get access_token + refresh_token
2. Use access_token in Authorization header
3. When expired → Use refresh_token to get new access_token
```

**Token Details:**
- **Access Token**: 15 minutes expiry
- **Refresh Token**: 7 days expiry
- **Header Format**: `Authorization: Bearer <token>`

### 2. Session-Based Authentication

**Flow:**
```
1. Session Login → Cookie automatically set
2. Cookie sent automatically with each request
3. Session stored in-memory (redis_json dict)
4. Logout → Session deleted from storage
```

**Session Details:**
- **Duration**: 30 minutes (1800 seconds)
- **Storage**: In-memory dictionary
- **Cookie Attributes**: `httponly`, `secure`, `samesite=strict`

---

## 💡 Usage Examples

### JWT Authentication

#### 1. JWT Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

#### 2. Access JWT-Protected Route
```bash
curl http://localhost:8000/m1/ \
  -H "Authorization: Bearer <your_access_token>"
```

#### 3. Refresh Access Token
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<your_refresh_token>"}'
```

---

### Session Authentication

#### 1. Session Login
```bash
curl -X POST http://localhost:8000/auth/session_log_in \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**
```json
{
  "message": "Login successful"
}
```
_Cookie `session_id` is automatically set_

#### 2. Access Session-Protected Route
```bash
curl http://localhost:8000/m3/ \
  --header 'Cookie: session_id=<your_session_id>'
```

#### 3. Rotate Session (Security Best Practice)
```bash
curl -X POST http://localhost:8000/auth/rotate_session \
  --header 'Cookie: session_id=<your_session_id>'
```

#### 4. Logout
```bash
curl -X POST http://localhost:8000/auth/session_log_out \
  --header 'Cookie: session_id=<your_session_id>'
```

---

## ⚙️ Configuration

Settings in `config.py`:

```python
# JWT Settings
SECRET_KEY = "your-secret-key"           # JWT signing key
REFRESH_SECRET_KEY = "refresh-secret"    # Refresh token key
ALGORITHM = "HS256"                      # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 15         # Access token TTL
REFRESH_TOKEN_EXPIRE_DAYS = 7            # Refresh token TTL

# Session Settings (in auth_routes.py)
SESSION_TTL = 30 * 60  # 30 minutes in seconds
```

> ⚠️ **Production Warning**: 
> - Use environment variables for secrets
> - Use real database (Redis/PostgreSQL) for sessions
> - Enable password hashing (bcrypt/argon2)
> - Use HTTPS in production (`secure=True` for cookies)

---

## 🧪 Demo Credentials

> ⚠️ **Note**: These are **demo credentials for learning only**!

Hardcoded users in `database.py`:

| Username | Password | Role | Status |
|----------|----------|------|--------|
| `admin` | `admin123` | admin | ✅ Active |
| `user1` | `password123` | user | ✅ Active |
| `test` | `test123` | user | ✅ Active |
| `inactive_user` | `inactive123` | user | ❌ Disabled |

**Production Requirements:**
- Use a real database (PostgreSQL, MongoDB, etc.)
- Hash passwords with bcrypt/argon2
- Implement proper user management
- Never store plain-text passwords

---

## 📚 Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PyJWT** | JWT encoding/decoding |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **Python** | Programming language |

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ JWT token-based authentication
- ✅ Session-based authentication with cookies
- ✅ Protected route implementation
- ✅ Security dependency injection
- ✅ Token refresh mechanism
- ✅ Session management (login/logout/rotate)
- ✅ FastAPI security best practices

---

<p align="center">
  Made with ❤️ while learning FastAPI Authentication
</p>

---

## 🚧 Coming SOON

### Google-Based Authentication & SSO Implementation

**Upcoming Features:**
- 🔐 **Google OAuth 2.0 Integration** - Sign in with Google
- 🏢 **Single Sign-On (SSO)** - Enterprise-ready authentication

Stay tuned for updates! 🎉
