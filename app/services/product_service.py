# app/services/product_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.crud.product import (
    get_product_by_id,
    get_all_products,
    get_featured_products,
    create_product,
    update_product,
    delete_product
)
from app.schemas.product import Product, ProductUpdate


def get_all(db: Session, category=None, search=None, in_stock=None, skip=0, limit=10):
    return get_all_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        search=search,
        in_stock=in_stock
    )


def get_one(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def get_featured(db: Session):
    return get_featured_products(db, limit=3)


def create(db: Session, product: Product):
    return create_product(db, product.model_dump())


def update(db: Session, product_id: int, updates: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = updates.model_dump(exclude_unset=True)
    return update_product(db, product_id, update_data)


def delete(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return delete_product(db, product_id)