# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create the engine — this is the connection to PostgreSQL
# app/db/database.py
engine = create_engine(
    settings.database_url,
    echo=settings.debug  # only log SQL when debug=True
)

# each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all your models will inherit from this
Base = declarative_base()


# ── Dependency ──────────────────────────────────────
def get_db():
    """
    FastAPI dependency — gives each route its own db session
    and closes it automatically when the request is done
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()