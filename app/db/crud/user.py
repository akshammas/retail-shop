# app/db/crud/user.py

from sqlalchemy.orm import Session, selectinload
from app.models import User
from app.core.security import hash_password


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .options(selectinload(User.orders))
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    role: str = "customer",
    phone_number: str = None
):
    hashed = hash_password(password)
    new_user = User(
        name=name,
        email=email,
        password=hashed,
        role=role,
        phone_number=phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, updates: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user