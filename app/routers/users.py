# app/routers/users.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserUpdate
from app.dependencies import get_current_user, require_admin
from app.db.database import get_db
from app.db.crud.user import (
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    update_user,
    delete_user
)
from app.core.security import hash_password

router = APIRouter()


# ── Own profile routes ──────────────────────────────

# get own profile
@router.get("/me/profile", response_model=UserResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


# update own profile
@router.put("/me/update", response_model=UserResponse)
async def update_my_profile(
    updates: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = {}

    if updates.name is not None:
        update_data["name"] = updates.name

    if updates.email is not None:
        # check email not taken by another user
        existing = get_user_by_email(db, updates.email)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        update_data["email"] = updates.email

    if updates.password is not None:
        update_data["password"] = hash_password(updates.password)

    updated = update_user(db, current_user.id, update_data)
    return updated


# delete own account
@router.delete("/me/delete")
async def delete_my_account(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_user(db, current_user.id)
    return {
        "message": f"Account for {deleted.email} has been deleted",
        "goodbye": f"Goodbye {deleted.name}!"
    }


# ── Admin routes ────────────────────────────────────

# list all users — admin only
@router.get("/", response_model=list[UserResponse])
async def list_users(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    users = get_all_users(db, skip=skip, limit=limit)
    return users


# get single user — admin only
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# delete any user — admin only
@router.delete("/{user_id}")
async def delete_user_by_admin(
    user_id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    # admin can't delete themselves this way
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account this way — use /users/me/delete"
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = delete_user(db, user_id)
    return {
        "message": "User deleted",
        "deleted_user": deleted.email
    }