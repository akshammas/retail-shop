# app/routers/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse, RefreshTokenRequest, AccessTokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.dependencies import get_current_user
from app.db.database import get_db
from app.db.crud.user import get_user_by_email, create_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "message": f"Welcome back {current_user.name}!"
    }


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):

    # check if email exists in real db
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create user in real db
    new_user = create_user(
        db=db,
        name=user.name,
        email=user.email,
        password=user.password,
        role="customer"
    )

    token_data = {"user_id": new_user.id, "role": new_user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }
    }


@router.post("/signup-admin", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup_admin(user: UserCreate, db: Session = Depends(get_db)):

    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(
        db=db,
        name=user.name,
        email=user.email,
        password=user.password,
        role="admin"
    )

    token_data = {"user_id": new_user.id, "role": new_user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):

    # find user in real db
    user = get_user_by_email(db, credentials.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"user_id": user.id, "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)):

    payload = verify_token(body.refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("user_id")
    from app.db.crud.user import get_user_by_id
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")

    token_data = {"user_id": user.id, "role": user.role}
    new_access_token = create_access_token(token_data)

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    return {
        "message": f"Goodbye {current_user.name}! Successfully logged out."
    }