# app/routers/categories.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.dependencies import get_current_user, require_admin
from app.db.database import get_db
from app.db.crud.category import (
    get_all_categories,
    get_category_by_id,
    get_category_by_name,
    create_category,
    update_category,
    delete_category
)
from typing import List

router = APIRouter()


# public — anyone can see categories
@router.get("/", response_model=List[CategoryResponse])
async def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# admin only — manage categories
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_new_category(
    category: CategoryCreate,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    existing = get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return create_category(db, category.name, category.description)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_existing_category(
    category_id: int,
    updates: CategoryUpdate,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    update_data = updates.model_dump(exclude_unset=True)
    updated = update_category(db, category_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}")
async def delete_existing_category(
    category_id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    deleted = delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": f"Category {deleted.name} deleted"}