# app/schemas/dashboard.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from app.schemas.order import OrderResponse


class RevenuePoint(BaseModel):
    date: str
    revenue: float


class LowStockProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    quantity: int


class TopSellingProduct(BaseModel):
    id: int
    name: str
    units_sold: int


class DashboardResponse(BaseModel):
    total_products: int
    total_users: int
    total_orders: int
    total_revenue: float
    today_revenue: float
    week_revenue: float
    this_week_revenue: float
    last_week_revenue: float
    revenue_percent_change: Optional[float] = None
    average_order_value: float
    new_users_this_week: int
    out_of_stock_count: int
    order_status_counts: Dict[str, int]
    revenue_chart: List[RevenuePoint]
    low_stock_products: List[LowStockProduct]
    top_selling_products: List[TopSellingProduct]
    recent_orders: List[OrderResponse]