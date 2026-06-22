# app/services/wishlist_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.crud.wishlist import (
    get_wishlist, get_wishlist_product_ids, add_to_wishlist, remove_from_wishlist,
)


def get_my_wishlist(db: Session, user_id: int):
    return get_wishlist(db, user_id)


def get_my_wishlist_ids(db: Session, user_id: int):
    return get_wishlist_product_ids(db, user_id)


def add(db: Session, user_id: int, product_id: int):
    return add_to_wishlist(db, user_id, product_id)


def remove(db: Session, user_id: int, product_id: int):
    item = remove_from_wishlist(db, user_id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not in wishlist")
    return item