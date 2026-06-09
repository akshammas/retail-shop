# app/db/init_db.py

from app.db.database import engine, Base
from app import models  # import models so Base knows about them


def create_tables():
    """Create all tables in PostgreSQL"""
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")


if __name__ == "__main__":
    create_tables()