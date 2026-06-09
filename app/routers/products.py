# app/routers/products.py

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.product import Product, ProductUpdate, ProductResponse
from app.dependencies import get_pagination, get_current_user, require_admin
from app.db.database import get_db
from app.db.crud.product import (
    get_product_by_id,
    get_all_products,
    get_featured_products,
    create_product,
    update_product,
    delete_product
)

router = APIRouter()


# ── Public routes ───────────────────────────────────

@router.get("/featured", response_model=list[ProductResponse])
async def get_featured(db: Session = Depends(get_db)):
    return get_featured_products(db, limit=3)


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    in_stock: Optional[bool] = None,
    pagination: dict = Depends(get_pagination),
    db: Session = Depends(get_db)
):
    products = get_all_products(
        db=db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        category=category,
        search=search,
        in_stock=in_stock
    )
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ── Admin routes ────────────────────────────────────

@router.get("/admin/all", response_model=list[ProductResponse])
async def admin_list_all(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    return get_all_products(db, skip=0, limit=1000)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(
    product: Product,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    product_data = product.model_dump()
    return create_product(db, product_data)


@router.put("/{id}", response_model=ProductResponse)
async def update_existing_product(
    id: int,
    updates: ProductUpdate,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    update_data = updates.model_dump(exclude_unset=True)
    updated = update_product(db, id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{id}")
async def delete_existing_product(
    id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    deleted = delete_product(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "message": "Product deleted",
        "deleted_by": admin_user.email,
        "product": deleted.name
    }