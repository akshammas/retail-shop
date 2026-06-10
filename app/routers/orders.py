# app/routers/orders.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.cart import CartItemAdd, CartItemResponse
from app.dependencies import get_current_user, require_admin
from app.db.database import get_db
from app.db.crud.order import (
    create_order,
    get_order_by_id,
    get_orders_by_user,
    get_all_orders,
    update_order_status
)
from app.db.crud.cart import (
    get_cart_items,
    add_to_cart,
    remove_from_cart,
    clear_cart
)
from typing import List

router = APIRouter()


# ── Cart routes ─────────────────────────────────────

@router.get("/cart", response_model=List[CartItemResponse])
async def view_cart(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_cart_items(db, current_user.id)


@router.post("/cart", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    item: CartItemAdd,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_to_cart(db, current_user.id, item.product_id, item.quantity)


@router.delete("/cart/{cart_item_id}")
async def remove_cart_item(
    cart_item_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = remove_from_cart(db, current_user.id, cart_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}


@router.delete("/cart")
async def clear_my_cart(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clear_cart(db, current_user.id)
    return {"message": "Cart cleared"}


# ── Order routes ────────────────────────────────────

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(
    order: OrderCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_order, error = create_order(
        db=db,
        user_id=current_user.id,
        shipping_address=order.shipping_address,
        items=order.items
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_order


@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_orders_by_user(db, current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # users can only see their own orders
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not your order")
    return order


# ── Admin order routes ──────────────────────────────

@router.get("/", response_model=List[OrderResponse])
async def list_all_orders(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    return get_all_orders(db, skip=skip, limit=limit)


@router.put("/{order_id}/status")
async def update_status(
    order_id: int,
    status: str,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    order = update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} status updated to {status}"}