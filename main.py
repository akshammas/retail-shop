# main.py

import httpx
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, users, orders
from app.routers import auth
from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.dependencies import verify_api_key

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

@app.get("/external-test")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()

@app.get("/token-test")
async def token_test():
    token = create_access_token(data={"user_id": 1, "role": "customer"})
    payload = verify_token(token)
    return {"token": token, "decoded": payload}

@app.get("/admin/stats", dependencies=[Depends(verify_api_key)])
async def get_stats():
    return {
        "total_products": 3,
        "total_users": len(auth.fake_users_db),
        "total_orders": 0
    }

# routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])