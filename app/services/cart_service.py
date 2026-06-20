# app/services/cart_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.crud.cart import (
    get_cart_items,
    add_to_cart,
    update_cart_item_quantity,
    remove_from_cart,
    clear_cart,
)


def get_cart(db: Session, user_id: int):
    return get_cart_items(db, user_id)


def add_item(db: Session, user_id: int, product_id: int, quantity: int):
    return add_to_cart(db, user_id, product_id, quantity)


def update_quantity(db: Session, user_id: int, cart_item_id: int, quantity: int):
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    item = update_cart_item_quantity(db, user_id, cart_item_id, quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


def remove_item(db: Session, user_id: int, cart_item_id: int):
    item = remove_from_cart(db, user_id, cart_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item


def clear(db: Session, user_id: int):
    clear_cart(db, user_id)