# app/schemas/product.py

from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import Optional, List
from datetime import datetime, timezone


class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    description: Optional[str] = None
    in_stock: bool = True
    quantity: int = Field(ge=0)
    category_id: Optional[int] = None
    brand: Optional[str] = None
    available_sizes: Optional[str] = None
    discount_percent: Optional[int] = Field(default=None, ge=1, le=90)
    discount_starts_at: Optional[datetime] = None
    discount_ends_at: Optional[datetime] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
    in_stock: Optional[bool] = None
    quantity: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    brand: Optional[str] = None
    available_sizes: Optional[str] = None
    discount_percent: Optional[int] = Field(default=None, ge=1, le=90)
    discount_starts_at: Optional[datetime] = None
    discount_ends_at: Optional[datetime] = None


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
    discount_percent: Optional[int] = None
    discount_starts_at: Optional[datetime] = None
    discount_ends_at: Optional[datetime] = None
    images: List[ProductImageResponse] = []

    @computed_field
    @property
    def is_on_sale(self) -> bool:
        if not self.discount_percent:
            return False
        now = datetime.now(timezone.utc)
        if self.discount_starts_at and now < self.discount_starts_at:
            return False
        if self.discount_ends_at and now > self.discount_ends_at:
            return False
        return True

    @computed_field
    @property
    def discounted_price(self) -> float:
        if self.is_on_sale:
            return round(self.price * (1 - self.discount_percent / 100), 2)
        return self.price