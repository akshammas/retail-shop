# main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, users, orders, categories, addresses,wishlist
from app.routers import auth
from app.core.config import settings
from app.dependencies import require_admin
from app.db.database import get_db
from app.db.crud.user import get_all_users
from app.db.crud.product import get_all_products
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

import os


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "debug": settings.debug
    }


@app.get("/admin/stats")
async def get_stats(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    all_users = get_all_users(db, skip=0, limit=1000)
    all_products = get_all_products(db, skip=0, limit=1000)
    return {
        "total_products": len(all_products),
        "total_users": len(all_users),
        "total_orders": 0,
        "requested_by": admin_user.email
    }


os.makedirs("static/images/products", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

app.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])
app.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])