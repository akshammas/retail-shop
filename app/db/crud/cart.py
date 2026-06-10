# app/db/crud/cart.py

from sqlalchemy.orm import Session
from app.models import CartItem


def get_cart_items(db: Session, user_id: int):
    """Get all cart items for a user"""
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    """Add item to cart or update quantity if already exists"""
    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing

    cart_item = CartItem(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_from_cart(db: Session, user_id: int, cart_item_id: int):
    """Remove a specific item from cart"""
    item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user_id
    ).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item


def clear_cart(db: Session, user_id: int):
    """Remove all items from user's cart"""
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()