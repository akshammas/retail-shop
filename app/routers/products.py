# app/routers/products.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.product import Product, ProductResponse
from app.dependencies import get_pagination, get_current_user, require_admin
from app.database import fake_products_db

router = APIRouter()
next_id = 4


@router.get("/featured")
async def get_featured():
    return {"message": "These are featured products"}


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    category: str = None,
    pagination: dict = Depends(get_pagination)
):
    products = list(fake_products_db.values())
    if category:
        products = [p for p in products if p["category"] == category]
    skip = pagination["skip"]
    limit = pagination["limit"]
    return products[skip: skip + limit]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    if product_id not in fake_products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_products_db[product_id]


# logged in users can create
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: Product,
    current_user: dict = Depends(get_current_user)
):
    global next_id
    new_product = {"id": next_id, **product.dict()}
    fake_products_db[next_id] = new_product
    next_id += 1
    return new_product


# logged in users can update
@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: int,
    product: Product,
    current_user: dict = Depends(get_current_user)
):
    if id not in fake_products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = {"id": id, **product.dict()}
    fake_products_db[id] = updated
    return updated


# ADMIN ONLY — delete
@router.delete("/{id}")
async def delete_product(
    id: int,
    admin_user: dict = Depends(require_admin)  # admin only
):
    if id not in fake_products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = fake_products_db.pop(id)
    return {
        "message": "Product deleted",
        "deleted_by": admin_user["email"],
        "deleted": deleted
    }