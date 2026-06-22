# app/db/crud/wishlist.py

from sqlalchemy.orm import Session, joinedload
from app.models import WishlistItem


def get_wishlist(db: Session, user_id: int):
    return (
        db.query(WishlistItem)
        .options(joinedload(WishlistItem.product))
        .filter(WishlistItem.user_id == user_id)
        .all()
    )


def get_wishlist_product_ids(db: Session, user_id: int):
    rows = db.query(WishlistItem.product_id).filter(WishlistItem.user_id == user_id).all()
    return [r[0] for r in rows]


def is_in_wishlist(db: Session, user_id: int, product_id: int) -> bool:
    return (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user_id, WishlistItem.product_id == product_id)
        .first()
        is not None
    )


def add_to_wishlist(db: Session, user_id: int, product_id: int):
    existing = (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user_id, WishlistItem.product_id == product_id)
        .first()
    )
    if existing:
        return existing

    item = WishlistItem(user_id=user_id, product_id=product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_from_wishlist(db: Session, user_id: int, product_id: int):
    item = (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user_id, WishlistItem.product_id == product_id)
        .first()
    )
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item