# app/routers/auth.py

from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter()

# fake users database
fake_users_db = {}
next_user_id = 1


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    global next_user_id

    # check if email already exists
    for existing_user in fake_users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    # hash password and store user
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

    # create tokens
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
    # find user by email
    user = None
    for u in fake_users_db.values():
        if u["email"] == credentials.email:
            user = u
            break

    # user not found
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # wrong password
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"  # same message — don't reveal which is wrong
        )

    # create tokens
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


@router.get("/me", response_model=UserResponse)
async def get_me():
    # placeholder — will add token verification in Day 18
    return {"id": 1, "name": "Test User", "email": "test@test.com", "role": "customer"}