# app/routers/users.py

from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password, verify_password

router = APIRouter()

# fake users database
fake_users_db = {}
next_user_id = 1


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    global next_user_id

    # check if email already exists
    for existing_user in fake_users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    # hash the password before storing
    hashed = hash_password(user.password)

    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "password": hashed,   # stored hashed ✅
        "role": "customer"
    }

    fake_users_db[next_user_id] = new_user
    next_user_id += 1

    return new_user


@router.post("/verify-password-test")
async def verify_test(email: str, password: str):
    # find user by email
    user = None
    for u in fake_users_db.values():
        if u["email"] == email:
            user = u
            break

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # verify password
    is_valid = verify_password(password, user["password"])

    return {
        "email": email,
        "password_valid": is_valid
    }