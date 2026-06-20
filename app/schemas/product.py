# app/schemas/product.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    description: Optional[str] = None
    in_stock: bool = True
    quantity: int = Field(ge=0)
    category_id: Optional[int] = None
    brand: Optional[str] = None
    available_sizes: Optional[str] = None   # "S,M,L,XL"


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
    in_stock: Optional[bool] = None
    quantity: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    brand: Optional[str] = None
    available_sizes: Optional[str] = None


class ProductImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    image_url: str
    is_primary: bool


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool
    quantity: int
    category_id: Optional[int] = None
    brand: Optional[str] = None
    available_sizes: Optional[str] = None
    images: List[ProductImageResponse] = []