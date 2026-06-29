# app/db/crud/dashboard.py

from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload, joinedload
from datetime import datetime, timedelta, timezone
from app.models import Order, OrderItem, Product, User


def get_total_counts(db: Session):
    """Real COUNT(*) queries — not limited to 1000 rows like before."""
    return {
        "total_products": db.query(Product).count(),
        "total_users": db.query(User).count(),
        "total_orders": db.query(Order).count(),
    }


def get_revenue_stats(db: Session):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)

    base = db.query(func.coalesce(func.sum(Order.total_amount), 0.0)).filter(
        Order.status != "cancelled"
    )

    total_revenue = base.scalar()
    today_revenue = base.filter(Order.created_at >= today_start).scalar()
    week_revenue = base.filter(Order.created_at >= week_start).scalar()

    return {
        "total_revenue": round(total_revenue, 2),
        "today_revenue": round(today_revenue, 2),
        "week_revenue": round(week_revenue, 2),
    }


def get_revenue_comparison(db: Session):
    now = datetime.now(timezone.utc)
    this_week_start = now - timedelta(days=7)
    last_week_start = now - timedelta(days=14)

    base = db.query(func.coalesce(func.sum(Order.total_amount), 0.0)).filter(
        Order.status != "cancelled"
    )

    this_week = base.filter(Order.created_at >= this_week_start).scalar()
    last_week = base.filter(
        Order.created_at >= last_week_start,
        Order.created_at < this_week_start,
    ).scalar()

    if last_week == 0:
        percent_change = None
    else:
        percent_change = round(((this_week - last_week) / last_week) * 100, 1)

    return {
        "this_week_revenue": round(this_week, 2),
        "last_week_revenue": round(last_week, 2),
        "revenue_percent_change": percent_change,
    }


def get_revenue_last_7_days(db: Session):
    now = datetime.now(timezone.utc)
    results = []
    for i in range(6, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        revenue = (
            db.query(func.coalesce(func.sum(Order.total_amount), 0.0))
            .filter(Order.status != "cancelled")
            .filter(Order.created_at >= day_start, Order.created_at < day_end)
            .scalar()
        )
        results.append({"date": day_start.strftime("%b %d"), "revenue": round(revenue, 2)})
    return results


def get_low_stock_products(db: Session, threshold: int = 10, limit: int = 5):
    return (
        db.query(Product)
        .filter(Product.quantity <= threshold, Product.quantity > 0)
        .order_by(Product.quantity.asc())
        .limit(limit)
        .all()
    )


def get_out_of_stock_count(db: Session):
    return db.query(Product).filter(Product.in_stock == False).count()


def get_recent_orders(db: Session, limit: int = 6):
    return (
        db.query(Order)
        .options(joinedload(Order.user), selectinload(Order.items).joinedload(OrderItem.product))
        .order_by(Order.created_at.desc())
        .limit(limit)
        .all()
    )


def get_order_status_counts(db: Session):
    rows = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    counts = {status: count for status, count in rows}
    for s in ["pending", "confirmed", "shipped", "delivered", "cancelled"]:
        counts.setdefault(s, 0)
    return counts


def get_top_selling_products(db: Session, limit: int = 5):
    results = (
        db.query(Product.id, Product.name, func.sum(OrderItem.quantity).label("units_sold"))
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status != "cancelled")
        .group_by(Product.id, Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return [{"id": r.id, "name": r.name, "units_sold": int(r.units_sold)} for r in results]


def get_new_users_this_week(db: Session):
    week_start = datetime.now(timezone.utc) - timedelta(days=7)
    return db.query(User).filter(User.created_at >= week_start).count()


def get_average_order_value(db: Session):
    result = (
        db.query(func.coalesce(func.avg(Order.total_amount), 0.0))
        .filter(Order.status != "cancelled")
        .scalar()
    )
    return round(result, 2)