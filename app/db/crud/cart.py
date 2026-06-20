# app/db/crud/cart.py

from sqlalchemy.orm import Session, joinedload
from app.models import CartItem


def get_cart_items(db: Session, user_id: int):
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .all()
    )


def get_cart_item_by_id(db: Session, user_id: int, cart_item_id: int):
    return (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id, CartItem.user_id == user_id)
        .first()
    )


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing

    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def update_cart_item_quantity(db: Session, user_id: int, cart_item_id: int, quantity: int):
    item = get_cart_item_by_id(db, user_id, cart_item_id)
    if not item:
        return None
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def remove_from_cart(db: Session, user_id: int, cart_item_id: int):
    item = get_cart_item_by_id(db, user_id, cart_item_id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item


def clear_cart(db: Session, user_id: int):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()