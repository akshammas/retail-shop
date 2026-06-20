# app/schemas/cart.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.product import ProductResponse


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    user_id: int
    product: ProductResponse   # ← nested, so frontend gets name/price/image in one call