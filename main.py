# main.py

import httpx
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, users, orders
from app.routers import auth
from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.dependencies import require_admin
from app.database import fake_users_db, fake_products_db

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
async def get_stats(admin_user: dict = Depends(require_admin)):
    return {
        "total_products": len(fake_products_db),
        "total_users": len(fake_users_db),
        "total_orders": 0,
        "requested_by": admin_user["email"]
    }


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])