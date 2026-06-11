# app/db/crud/image.py

from sqlalchemy.orm import Session
from app.models import ProductImage
import os


def get_images_by_product(db: Session, product_id: int):
    """Get all images for a product"""
    return db.query(ProductImage).filter(
        ProductImage.product_id == product_id
    ).all()


def get_image_by_id(db: Session, image_id: int):
    """Get single image by id"""
    return db.query(ProductImage).filter(
        ProductImage.id == image_id
    ).first()


def get_primary_image(db: Session, product_id: int):
    """Get primary image for a product"""
    return db.query(ProductImage).filter(
        ProductImage.product_id == product_id,
        ProductImage.is_primary == True
    ).first()


def add_image(db: Session, product_id: int, image_url: str, is_primary: bool = False):
    """Add an image to a product"""

    # if this is set as primary, unset all others
    if is_primary:
        db.query(ProductImage).filter(
            ProductImage.product_id == product_id
        ).update({"is_primary": False})
        db.commit()

    # if no images exist yet, make this one primary automatically
    existing_count = db.query(ProductImage).filter(
        ProductImage.product_id == product_id
    ).count()

    if existing_count == 0:
        is_primary = True

    image = ProductImage(
        product_id=product_id,
        image_url=image_url,
        is_primary=is_primary
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def set_primary_image(db: Session, image_id: int, product_id: int):
    """Set an image as primary"""
    # unset all primary
    db.query(ProductImage).filter(
        ProductImage.product_id == product_id
    ).update({"is_primary": False})

    # set new primary
    image = get_image_by_id(db, image_id)
    if not image:
        return None
    image.is_primary = True
    db.commit()
    db.refresh(image)
    return image


def delete_image(db: Session, image_id: int):
    """Delete an image and its file from disk"""
    image = get_image_by_id(db, image_id)
    if not image:
        return None

    # delete file from disk
    filepath = image.image_url.lstrip("/")
    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(image)
    db.commit()
    return image


def delete_all_product_images(db: Session, product_id: int):
    """Delete all images for a product"""
    images = get_images_by_product(db, product_id)
    for image in images:
        filepath = image.image_url.lstrip("/")
        if os.path.exists(filepath):
            os.remove(filepath)
        db.delete(image)
    db.commit()