# app/services/order_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.crud.order import (
    create_order,
    get_order_by_id,
    get_orders_by_user,
    get_all_orders,
    update_order_status
)
from app.db.crud.cart import get_cart_items, clear_cart
from app.schemas.order import OrderCreate


VALID_STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled"]


def place_order(db: Session, user_id: int, order: OrderCreate):
    new_order, error = create_order(
        db=db,
        user_id=user_id,
        shipping_address=order.shipping_address,
        items=order.items
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_order


def place_order_from_cart(db: Session, user_id: int, shipping_address: str):
    """Place order using items currently in cart"""
    cart_items = get_cart_items(db, user_id)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # convert cart items to order items format
    from app.schemas.order import OrderItemCreate
    items = [
        OrderItemCreate(product_id=item.product_id, quantity=item.quantity)
        for item in cart_items
    ]

    new_order, error = create_order(
        db=db,
        user_id=user_id,
        shipping_address=shipping_address,
        items=items
    )
    if error:
        raise HTTPException(status_code=400, detail=error)

    # clear cart after successful order
    clear_cart(db, user_id)

    return new_order


def get_my_orders(db: Session, user_id: int):
    return get_orders_by_user(db, user_id)


def get_one(db: Session, order_id: int, user_id: int, is_admin: bool = False):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not is_admin and order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your order")
    return order


def get_all(db: Session, skip: int = 0, limit: int = 10):
    return get_all_orders(db, skip=skip, limit=limit)


def change_status(db: Session, order_id: int, new_status: str):
    if new_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {VALID_STATUSES}"
        )
    order = update_order_status(db, order_id, new_status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def place_order_direct(db: Session, user_id: int, shipping_address: str, items: list):
    """Place an order from an explicit item list — does NOT touch the cart at all."""
    new_order, error = create_order(
        db=db,
        user_id=user_id,
        shipping_address=shipping_address,
        items=items,
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_order