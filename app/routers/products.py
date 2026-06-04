# app/routers/products.py — add Depends to write routes

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.product import Product, ProductResponse
from app.dependencies import get_pagination

router = APIRouter()

fake_db = {
    1: {"id": 1, "name": "T-shirt", "price": 499.99, "quantity": 10, "category": "general", "description": "Cotton round neck", "in_stock": True},
    2: {"id": 2, "name": "Shirt", "price": 999.99, "quantity": 5, "category": "general", "description": "Formal shirt", "in_stock": True},
    3: {"id": 3, "name": "Shorts", "price": 299.99, "quantity": 20, "category": "general", "description": "Sports shorts", "in_stock": True},
}

next_id = 4


def get_current_user_dep():
    from app.dependencies import get_current_user
    return get_current_user


@router.get("/featured")
async def get_featured():
    return {"message": "These are featured products"}


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    category: str = None,
    pagination: dict = Depends(get_pagination)
):
    products = list(fake_db.values())
    if category:
        products = [p for p in products if p["category"] == category]
    skip = pagination["skip"]
    limit = pagination["limit"]
    return products[skip: skip + limit]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_db[product_id]


# protected — must be logged in
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: Product,
    current_user: dict = Depends(get_current_user_dep())
):
    global next_id
    new_product = {"id": next_id, **product.dict()}
    fake_db[next_id] = new_product
    next_id += 1
    return new_product


@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: int,
    product: Product,
    current_user: dict = Depends(get_current_user_dep())
):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = {"id": id, **product.dict()}
    fake_db[id] = updated
    return updated


@router.delete("/{id}")
async def delete_product(
    id: int,
    current_user: dict = Depends(get_current_user_dep())
):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = fake_db.pop(id)
    return {"message": "Product deleted", "deleted": deleted}