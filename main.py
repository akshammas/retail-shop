# main.py

import httpx
from fastapi import FastAPI
from app.routers import products, users, orders

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to my retail shop"}


@app.get("/external-test")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()


# include routers with prefixes
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

