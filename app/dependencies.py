# app/dependencies.py

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.security import verify_token
from app.database import fake_users_db  # from database.py now


def get_pagination(skip: int = 0, limit: int = 10):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    return {"skip": skip, "limit": limit}


def get_settings():
    return settings


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.secret_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    if payload.get("type") != "access":
        raise credentials_exception

    user_id = payload.get("user_id")
    user = fake_users_db.get(user_id)

    if user is None:
        raise credentials_exception

    return user