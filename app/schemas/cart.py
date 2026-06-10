# app/schemas/cart.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    user_id: int