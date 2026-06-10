# app/db/init_db.py

from app.db.database import engine, Base, SessionLocal
from app import models
from app.db.crud.product import seed_products
from app.db.crud.category import seed_categories


def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")


def seed():
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_products(db)
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    seed()