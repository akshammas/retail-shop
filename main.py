# main.py

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, users, orders
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)


# ── CORS Middleware ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,   # list from .env
    allow_credentials=True,
    allow_methods=["*"],                   # GET, POST, PUT, DELETE etc
    allow_headers=["*"],                   # Authorization, Content-Type etc
)


# ── Routes ─────────────────────────────────────────
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


# ── Routers ────────────────────────────────────────
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])