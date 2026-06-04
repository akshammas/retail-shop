# app/dependencies.py

# Shared dependencies go here
# Example: get current user, get db session

# app/dependencies.py

from fastapi import Depends, HTTPException, Header
from app.core.config import settings


# ── Pagination dependency ───────────────────────────
def get_pagination(skip: int = 0, limit: int = 10):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    return {"skip": skip, "limit": limit}


# ── Settings dependency ─────────────────────────────
def get_settings():
    return settings


# ── API key dependency (simple auth for now) ────────
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.secret_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key
    