# app/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.crud.user import (
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    update_user,
    delete_user
)
from app.core.security import hash_password
from app.schemas.user import UserUpdate


def get_all(db: Session, skip: int = 0, limit: int = 10):
    return get_all_users(db, skip=skip, limit=limit)


def get_one(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_profile(db: Session, user_id: int, updates: UserUpdate):
    update_data = {}

    if updates.name is not None:
        update_data["name"] = updates.name

    if updates.email is not None:
        existing = get_user_by_email(db, updates.email)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already in use")
        update_data["email"] = updates.email

    if updates.password is not None:
        update_data["password"] = hash_password(updates.password)

    return update_user(db, user_id, update_data)


def delete_account(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, user_id)