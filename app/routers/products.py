# app/routers/products.py — routes become thin

from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.product import Product, ProductUpdate, ProductResponse, ProductImageResponse
from app.dependencies import get_pagination, get_current_user, require_admin
from app.db.database import get_db
from app.db.crud.image import (
    get_images_by_product,
    add_image,
    set_primary_image,
    delete_image,
    delete_all_product_images
)
from app.db.crud.product import get_product_by_id
from app import services
import app.services.product_service as product_service
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "static/images/products"
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_SIZE_MB = 5


@router.get("/featured", response_model=List[ProductResponse])
async def get_featured(db: Session = Depends(get_db)):
    return product_service.get_featured(db)


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    in_stock: Optional[bool] = None,
    pagination: dict = Depends(get_pagination),
    db: Session = Depends(get_db)
):
    return product_service.get_all(
        db=db,
        category=category,
        search=search,
        in_stock=in_stock,
        skip=pagination["skip"],
        limit=pagination["limit"]
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_one(db, product_id)


@router.get("/admin/all", response_model=List[ProductResponse])
async def admin_list_all(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    return product_service.get_all(db, skip=0, limit=1000)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(
    product: Product,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    return product_service.create(db, product)


@router.put("/{id}", response_model=ProductResponse)
async def update_existing_product(
    id: int,
    updates: ProductUpdate,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    return product_service.update(db, id, updates)


@router.delete("/{id}")
async def delete_existing_product(
    id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    deleted = product_service.delete(db, id)
    return {
        "message": "Product deleted",
        "deleted_by": admin_user.email,
        "product": deleted.name
    }


# ── Image routes ────────────────────────────────────

@router.get("/{product_id}/images", response_model=List[ProductImageResponse])
async def get_product_images(product_id: int, db: Session = Depends(get_db)):
    product_service.get_one(db, product_id)
    return get_images_by_product(db, product_id)


@router.post("/{product_id}/images", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    is_primary: bool = False,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    product_service.get_one(db, product_id)

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG and WebP allowed")

    contents = await file.read()
    if len(contents) / (1024 * 1024) > MAX_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Max {MAX_SIZE_MB}MB allowed")

    extension = file.filename.split(".")[-1].lower()
    filename = f"product_{product_id}_{uuid.uuid4().hex[:8]}.{extension}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(contents)

    image_url = f"/static/images/products/{filename}"
    return add_image(db, product_id, image_url, is_primary)


@router.patch("/{product_id}/images/{image_id}/set-primary", response_model=ProductImageResponse)
async def set_image_as_primary(
    product_id: int,
    image_id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    image = set_primary_image(db, image_id, product_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.delete("/{product_id}/images/{image_id}")
async def delete_single_image(
    product_id: int,
    image_id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    image = delete_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}


@router.delete("/{product_id}/images")
async def delete_all_images(
    product_id: int,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    product_service.get_one(db, product_id)
    delete_all_product_images(db, product_id)
    return {"message": "All images deleted"}