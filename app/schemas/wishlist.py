# app/schemas/wishlist.py

from pydantic import BaseModel, ConfigDict
from app.schemas.product import ProductResponse


class WishlistAdd(BaseModel):
    product_id: int


class WishlistItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product: ProductResponse