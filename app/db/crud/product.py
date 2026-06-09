# app/db/crud/product.py

from sqlalchemy.orm import Session
from app.models import Product


def get_product_by_id(db: Session, product_id: int):
    """Get single product by id"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_all_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category: str = None,
    search: str = None,
    in_stock: bool = None
):
    """Get all products with optional filters"""
    query = db.query(Product)

    # filter by category
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    # filter by search term in name or description
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%") |
            Product.description.ilike(f"%{search}%")
        )

    # filter by stock status
    if in_stock is not None:
        query = query.filter(Product.in_stock == in_stock)

    return query.offset(skip).limit(limit).all()


def get_featured_products(db: Session, limit: int = 3):
    """Get in-stock products for featured section"""
    return db.query(Product).filter(Product.in_stock == True).limit(limit).all()


def create_product(db: Session, product_data: dict):
    """Create a new product"""
    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(db: Session, product_id: int, updates: dict):
    """Update product fields"""
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    for key, value in updates.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    """Delete a product"""
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product


def seed_products(db: Session):
    """Add initial products if table is empty"""
    count = db.query(Product).count()
    if count == 0:
        initial_products = [
            Product(name="T-shirt", price=499.99, quantity=10, category="general", description="Cotton round neck", in_stock=True),
            Product(name="Shirt", price=999.99, quantity=5, category="general", description="Formal shirt", in_stock=True),
            Product(name="Shorts", price=299.99, quantity=20, category="general", description="Sports shorts", in_stock=True),
        ]
        db.add_all(initial_products)
        db.commit()
        print("✅ Products seeded!")
    else:
        print(f"Products table already has {count} rows — skipping seed")