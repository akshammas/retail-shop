# test_db_connection.py  ← temporary file, delete after testing

from app.db.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()
        print(f"✅ Connected to PostgreSQL!")
        print(f"Version: {version[0]}")
except Exception as e:
    print(f"❌ Connection failed: {e}")