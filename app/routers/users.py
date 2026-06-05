# app/routers/users.py

from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.dependencies import get_current_user
from app.database import fake_users_db

router = APIRouter()


@router.get("/", )
async def list_users(current_user: dict = Depends(get_current_user)):
    # only logged in users can see this
    users = [
        {"id": u["id"], "name": u["name"], "email": u["email"], "role": u["role"]}
        for u in fake_users_db.values()
    ]
    return users


@router.get("/{user_id}")
async def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    user = fake_users_db.get(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}