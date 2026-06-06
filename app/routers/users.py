# app/routers/users.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserResponse, UserUpdate
from app.dependencies import get_current_user, require_admin
from app.database import fake_users_db
from app.core.security import hash_password

router = APIRouter()


# ── Admin routes ────────────────────────────────────

# list all users — admin only
@router.get("/", response_model=list[UserResponse])
async def list_users(admin_user: dict = Depends(require_admin)):
    users = [
        {
            "id": u["id"],
            "name": u["name"],
            "email": u["email"],
            "role": u["role"]
        }
        for u in fake_users_db.values()
    ]
    return users


# get single user — admin only
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, admin_user: dict = Depends(require_admin)):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# delete any user — admin only
@router.delete("/{user_id}")
async def delete_user(user_id: int, admin_user: dict = Depends(require_admin)):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # admin can't delete themselves
    if user_id == admin_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account this way — use /users/me/delete"
        )
    deleted = fake_users_db.pop(user_id)
    return {
        "message": "User deleted",
        "deleted_user": deleted["email"]
    }


# ── Own profile routes ──────────────────────────────

# get own profile
@router.get("/me/profile", response_model=UserResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user


# update own profile
@router.put("/me/update", response_model=UserResponse)
async def update_my_profile(
    updates: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]
    user = fake_users_db[user_id]

    # only update fields that were actually sent
    if updates.name is not None:
        user["name"] = updates.name

    if updates.email is not None:
        # check email not taken by another user
        for u in fake_users_db.values():
            if u["email"] == updates.email and u["id"] != user_id:
                raise HTTPException(
                    status_code=400,
                    detail="Email already in use"
                )
        user["email"] = updates.email

    if updates.password is not None:
        user["password"] = hash_password(updates.password)

    fake_users_db[user_id] = user
    return user


# delete own account
@router.delete("/me/delete")
async def delete_my_account(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    deleted = fake_users_db.pop(user_id)
    return {
        "message": f"Account for {deleted['email']} has been deleted",
        "goodbye": f"Goodbye {deleted['name']}!"
    }