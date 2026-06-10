# app/db/crud/category.py

from sqlalchemy.orm import Session
from app.models import Category


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, name: str, description: str = None):
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, updates: dict):
    category = get_category_by_id(db, category_id)
    if not category:
        return None
    for key, value in updates.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category


def seed_categories(db: Session):
    count = db.query(Category).count()
    if count == 0:
        initial = [
            Category(name="general", description="General products"),
            Category(name="clothing", description="Clothes and apparel"),
            Category(name="outerwear", description="Jackets and coats"),
            Category(name="footwear", description="Shoes and sandals"),
            Category(name="accessories", description="Belts, bags, and more"),
        ]
        db.add_all(initial)
        db.commit()
        print("✅ Categories seeded!")