# app/schemas/order.py

from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime          # ← add this import
from app.schemas.product import ProductResponse


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    product: ProductResponse


class OrderCreate(BaseModel):
    shipping_address: str
    items: List[OrderItemCreate]


class BuyNowRequest(BaseModel):
    shipping_address: str
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    total_amount: float
    shipping_address: Optional[str] = None
    created_at: Optional[datetime] = None   # ← was `str`, now correctly `datetime`
    items: List[OrderItemResponse] = []