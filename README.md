# 🔐 Auth API

A **FastAPI-based authentication system** implementing JWT (JSON Web Tokens) for secure API access.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Authentication Flow](#-authentication-flow)
- [Usage Examples](#-usage-examples)
- [Configuration](#️-configuration)
- [Roadmap](#-roadmap)

---

## ✨ Features

### Current Implementation ✅
- **JWT-based Authentication** - Secure token-based auth
- **Access & Refresh Tokens** - Short-lived access + long-lived refresh tokens
- **Protected Routes** - Security middleware for route protection
- **Modular Architecture** - Clean separation of concerns
- **User Role Support** - Role included in token payload

### Coming Soon 🚧
- [ ] **SSO (Single Sign-On)** - Enterprise authentication
- [ ] **Google OAuth 2.0** - Sign in with Google
- [ ] **Password Hashing** - bcrypt/argon2 implementation
- [ ] **Rate Limiting** - API rate limiting
- [ ] **Token Blacklisting** - Logout/revoke tokens

---

## 📁 Project Structure

```
Auth/
├── main.py              # 🚀 App entry point
├── config.py            # ⚙️ Configuration settings
├── database.py          # 🗄️ User database & auth helpers
├── models.py            # 📦 Pydantic models
├── auth.py              # 🔐 JWT token utilities
├── dependencies.py      # 🛡️ Security dependencies
├── routes/
│   ├── auth_routes.py   # 🔑 Login & refresh endpoints
│   └── general_routes.py# 🏠 Health & root endpoints
├── m1/                  # 🔒 Protected module (requires auth)
└── m2/                  # 🌐 Public module (no auth)
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

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/` | ❌ | Welcome message |
| `GET` | `/health` | ❌ | Health check |
| `POST` | `/auth/login` | ❌ | Login & get tokens |
| `POST` | `/auth/refresh` | ❌ | Refresh access token |
| `*` | `/m1/*` | ✅ | Protected routes |
| `*` | `/m2/*` | ❌ | Public routes |

---

## 🔄 Authentication Flow

```
┌─────────────┐      POST /auth/login       ┌─────────────┐
│   Client    │ ───────────────────────────▶│   Server    │
│             │   {username, password}      │             │
└─────────────┘                             └─────────────┘
       │                                           │
       │◀──────────────────────────────────────────│
       │    {access_token, refresh_token}          │
       │                                           │
       │    GET /protected-route                   │
       │    Authorization: Bearer <access_token>   │
       │──────────────────────────────────────────▶│
       │                                           │
       │◀──────────────────────────────────────────│
       │         { protected_data }                │
       │                                           │
       │ ─ ─ ─ Access Token Expires ─ ─ ─ ─ ─ ─ ─ │
       │                                           │
       │    POST /auth/refresh                     │
       │    {refresh_token}                        │
       │──────────────────────────────────────────▶│
       │                                           │
       │◀──────────────────────────────────────────│
       │    {new_access_token}                     │
       ▼                                           ▼
```

### Token Types

| Token | Purpose | Expiration | Secret Key |
|-------|---------|------------|------------|
| **Access Token** | API access | 15 minutes | `SECRET_KEY` |
| **Refresh Token** | Get new access token | 7 days | `REFRESH_SECRET_KEY` |

---

## 💡 Usage Examples

### 1. Login

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

### 2. Access Protected Route

```bash
curl http://localhost:8000/m1/your-endpoint \
  -H "Authorization: Bearer <your_access_token>"
```

### 3. Refresh Token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<your_refresh_token>"}'
```

---

## ⚙️ Configuration

Settings are in `config.py`:

```python
SECRET_KEY = "your-secret-key"           # JWT signing key
REFRESH_SECRET_KEY = "refresh-secret"    # Refresh token key
ALGORITHM = "HS256"                      # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 15         # Access token TTL
REFRESH_TOKEN_EXPIRE_DAYS = 7            # Refresh token TTL
```

> ⚠️ **Production**: Use environment variables for secrets!

---

## 🧪 Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | admin |
| `user1` | `password123` | user |
| `test` | `test123` | user |

---

## 🗺️ Roadmap

### Phase 1: Core Auth ✅
- [x] JWT Access Tokens
- [x] JWT Refresh Tokens
- [x] Protected Routes
- [x] Modular Code Structure

### Phase 2: Enhanced Security 🔜
- [ ] Password Hashing (bcrypt/argon2)
- [ ] Token Blacklisting (Redis)
- [ ] Rate Limiting
- [ ] CORS Configuration

### Phase 3: SSO & OAuth 📅
- [ ] **Google OAuth 2.0** - Sign in with Google
- [ ] **GitHub OAuth** - Sign in with GitHub
- [ ] **Microsoft SSO** - Enterprise SSO
- [ ] **SAML 2.0 Support** - Enterprise identity providers

### Phase 4: Advanced Features 🔮
- [ ] Multi-Factor Authentication (MFA)
- [ ] Email Verification
- [ ] Password Reset Flow
- [ ] Session Management
- [ ] Audit Logging

---

## 📚 Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PyJWT** | JWT encoding/decoding |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is for learning purposes.

---

<p align="center">
  Made with ❤️ while learning FastAPI Authentication
</p>
