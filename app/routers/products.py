# app/routers/products.py

from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas.product import Product, ProductUpdate, ProductResponse
from app.dependencies import get_pagination, get_current_user, require_admin
from app.database import fake_products_db
from typing import Optional

router = APIRouter()
next_id = 4


# ── Public routes ───────────────────────────────────

# featured products — specific route first
@router.get("/featured", response_model=list[ProductResponse])
async def get_featured():
    featured = [p for p in fake_products_db.values() if p["in_stock"]]
    return featured[:3]


# list all products — public, paginated, filterable, searchable
@router.get("/", response_model=list[ProductResponse])
async def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    in_stock: Optional[bool] = None,
    pagination: dict = Depends(get_pagination)
):
    products = list(fake_products_db.values())

    # filter by category
    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]

    # filter by search term in name or description
    if search:
        products = [
            p for p in products
            if search.lower() in p["name"].lower()
            or (p["description"] and search.lower() in p["description"].lower())
        ]

    # filter by stock status
    if in_stock is not None:
        products = [p for p in products if p["in_stock"] == in_stock]

    skip = pagination["skip"]
    limit = pagination["limit"]
    return products[skip: skip + limit]


# get single product — public
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    if product_id not in fake_products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_products_db[product_id]


# ── Admin routes ────────────────────────────────────

# admin view all products including out of stock
@router.get("/admin/all", response_model=list[ProductResponse])
async def admin_list_all(admin_user: dict = Depends(require_admin)):
    return list(fake_products_db.values())


# create product — admin only
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: Product,
    admin_user: dict = Depends(require_admin)
):
    global next_id
    new_product = {"id": next_id, **product.model_dump()}
    fake_products_db[next_id] = new_product
    next_id += 1
    return new_product


# update product — admin only
@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: int,
    updates: ProductUpdate,
    admin_user: dict = Depends(require_admin)
):
    if id not in fake_products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product = fake_products_db[id]

    # only update fields that were sent
    update_data = updates.model_dump(exclude_unset=True)
    product.update(update_data)
    fake_products_db[id] = product

    return product


# delete product — admin only
@router.delete("/{id}")
async def delete_product(
    id: int,
    admin_user: dict = Depends(require_admin)
):
    if id not in fake_products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = fake_products_db.pop(id)
    return {
        "message": "Product deleted",
        "deleted_by": admin_user["email"],
        "deleted": deleted
    }