# app/routers/orders.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_orders():
    return {"message": "orders route - coming soon"}