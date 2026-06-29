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
from app.models import Order
from app.schemas.dashboard import DashboardResponse
from app.db.crud.dashboard import (
    get_total_counts, get_revenue_stats, get_revenue_comparison,
    get_revenue_last_7_days, get_low_stock_products, get_out_of_stock_count,
    get_recent_orders, get_order_status_counts, get_top_selling_products,
    get_new_users_this_week, get_average_order_value,
)
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


@app.get("/admin/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    counts = get_total_counts(db)          # ← real COUNT(*), fixes the 1000 cap
    revenue = get_revenue_stats(db)
    comparison = get_revenue_comparison(db)

    return {
        **counts,
        **revenue,
        **comparison,
        "average_order_value": get_average_order_value(db),
        "new_users_this_week": get_new_users_this_week(db),
        "out_of_stock_count": get_out_of_stock_count(db),
        "order_status_counts": get_order_status_counts(db),
        "revenue_chart": get_revenue_last_7_days(db),
        "low_stock_products": get_low_stock_products(db),
        "top_selling_products": get_top_selling_products(db),
        "recent_orders": get_recent_orders(db),
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