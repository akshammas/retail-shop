# app/schemas/product.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="Must be greater than 0")
    description: Optional[str] = None
    in_stock: bool = True
    quantity: int = Field(ge=0, description="Must be 0 or more")
    category: str = Field(default="general")


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
    in_stock: Optional[bool] = None
    quantity: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = None


class ProductResponse(Product):
    model_config = ConfigDict(from_attributes=True)
    id: int