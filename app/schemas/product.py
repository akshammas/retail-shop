# app/schemas/product.py

from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="Must be greater than 0")
    description: Optional[str] = None
    in_stock: bool = True
    quantity: int = Field(ge=0, description="Must be 0 or more")
    category: str = Field(default="general")


class ProductResponse(Product):
    id: int  # response includes the id