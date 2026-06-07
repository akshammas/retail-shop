# app/core/security.py

import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings


# ── Password hashing ────────────────────────────────
# bcrypt automatically salts passwords — same password hashes differently each time
# verify_password handles the comparison securely

def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ── Token creation ──────────────────────────────────
# Access tokens: short lived (30 min) — used for API requests
# Refresh tokens: long lived (7 days) — used to get new access tokens

def create_access_token(data: dict) -> str:
    """Create a short-lived JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict) -> str:
    """Create a long-lived JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


# ── Token verification ──────────────────────────────
def verify_token(token: str) -> dict:
    """Decode and verify a JWT token. Returns None if invalid or expired."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None