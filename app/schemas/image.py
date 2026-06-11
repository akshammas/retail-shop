# app/schemas/image.py

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    image_url: str
    is_primary: bool