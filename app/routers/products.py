# app/routers/products.py

from fastapi import APIRouter, HTTPException, status
from app.schemas.product import Product, ProductResponse  # updated import

router = APIRouter()

fake_db = {
    1: {"id": 1, "name": "T-shirt", "price": 499.99, "quantity": 10, "category": "general", "description": "Cotton round neck", "in_stock": True},
    2: {"id": 2, "name": "Shirt", "price": 999.99, "quantity": 5, "category": "general", "description": "Formal shirt", "in_stock": True},
    3: {"id": 3, "name": "Shorts", "price": 299.99, "quantity": 20, "category": "general", "description": "Sports shorts", "in_stock": True},
}

next_id = 4


@router.get("/featured")
async def get_featured():
    return {"message": "These are featured products"}


@router.get("/", response_model=list[ProductResponse])
async def list_products(category: str = None, limit: int = 10):
    products = list(fake_db.values())
    if category:
        products = [p for p in products if p["category"] == category]
    return products[:limit]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_db[product_id]


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    global next_id
    new_product = {"id": next_id, **product.dict()}
    fake_db[next_id] = new_product
    next_id += 1
    return new_product


@router.put("/{id}", response_model=ProductResponse)
async def update_product(id: int, product: Product):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = {"id": id, **product.dict()}
    fake_db[id] = updated
    return updated


@router.delete("/{id}")
async def delete_product(id: int):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = fake_db.pop(id)
    return {"message": "Product deleted", "deleted": deleted}