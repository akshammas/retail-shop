# app/schemas/order.py

from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.models import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderCreate(BaseModel):
    shipping_address: str
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    total_amount: float
    shipping_address: Optional[str] = None
    items: List[OrderItemResponse] = []

class BuyNowRequest(BaseModel):
    shipping_address: str
    items: List[OrderItemCreate] 