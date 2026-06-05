# app/routers/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.dependencies import get_current_user
from app.database import fake_users_db  # from database.py now

router = APIRouter()
next_user_id = 1


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "message": f"Welcome back {current_user['name']}!"
    }


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    global next_user_id

    for existing_user in fake_users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "password": hashed,
        "role": "customer"
    }
    fake_users_db[next_user_id] = new_user
    next_user_id += 1

    token_data = {"user_id": new_user["id"], "role": new_user["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"]
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user = None
    for u in fake_users_db.values():
        if u["email"] == credentials.email:
            user = u
            break

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"user_id": user["id"], "role": user["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }


@router.post("/signup-admin", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup_admin(user: UserCreate):
    global next_user_id

    for existing_user in fake_users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "password": hashed,
        "role": "admin"  # admin role set here
    }
    fake_users_db[next_user_id] = new_user
    next_user_id += 1

    token_data = {"user_id": new_user["id"], "role": new_user["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"]
        }
    }
