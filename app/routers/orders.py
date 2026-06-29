# app/routers/orders.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.cart import CartItemAdd, CartItemResponse,CartItemUpdate
from app.dependencies import get_current_user, require_admin
from app.db.database import get_db
import app.services.order_service as order_service
import app.services.cart_service as cart_service
from typing import List
from pydantic import BaseModel
from app.schemas.order import BuyNowRequest

router = APIRouter()


class CheckoutRequest(BaseModel):
    shipping_address: str


# ── Cart routes ─────────────────────────────────────

@router.get("/cart", response_model=List[CartItemResponse])
async def view_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return cart_service.get_cart(db, current_user.id)


@router.post("/cart", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    item: CartItemAdd,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.add_item(db, current_user.id, item.product_id, item.quantity)


@router.put("/cart/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
    cart_item_id: int,
    body: CartItemUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.update_quantity(db, current_user.id, cart_item_id, body.quantity)


@router.delete("/cart/{cart_item_id}")
async def remove_cart_item(
    cart_item_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_service.remove_item(db, current_user.id, cart_item_id)
    return {"message": "Item removed from cart"}


@router.delete("/cart")
async def clear_my_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    cart_service.clear(db, current_user.id)
    return {"message": "Cart cleared"}

# ── Checkout from cart ──────────────────────────────

@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def checkout_from_cart(
    body: CheckoutRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Place order directly from cart items"""
    return order_service.place_order_from_cart(
        db=db,
        user_id=current_user.id,
        shipping_address=body.shipping_address
    )


# ── Order routes ────────────────────────────────────

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(
    order: OrderCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return order_service.place_order(db, current_user.id, order)


@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return order_service.get_my_orders(db, current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role == "admin"
    return order_service.get_one(db, order_id, current_user.id, is_admin)


@router.get("/", response_model=List[OrderResponse])
async def list_all_orders(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    status: str = None,
):
    return order_service.get_all(db, skip=skip, limit=limit, status=status)


@router.put("/{order_id}/status")
async def update_status(
    order_id: int,
    status: str,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    order = order_service.change_status(db, order_id, status)
    return {"message": f"Order {order_id} status updated to {status}"}



@router.post("/buy-now", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def buy_now_checkout(
    body: BuyNowRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Order specific items directly, bypassing the cart entirely."""
    return order_service.place_order_direct(
        db=db,
        user_id=current_user.id,
        shipping_address=body.shipping_address,
        items=body.items,
    )