from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import httpx

app = FastAPI()

# ── Model ──────────────────────────────────────────
class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="Must be greater than 0")
    description: Optional[str] = None
    in_stock: bool = True
    quantity: int = Field(ge=0, description="Must be 0 or more")
    category: str = Field(default="general")


# ── Fake database ──────────────────────────────────
fake_db = {
    1: {"name": "T-shirt", "price": 499.99, "quantity": 10, "category": "general", "description": "Cotton round neck", "in_stock": True},
    2: {"name": "Shirt", "price": 999.99, "quantity": 5, "category": "general", "description": "Formal shirt", "in_stock": True},
    3: {"name": "Shorts", "price": 299.99, "quantity": 20, "category": "general", "description": "Sports shorts", "in_stock": True},
}

# auto increment id tracker
next_id = 4


# ── Routes ─────────────────────────────────────────

# Home
@app.get("/")
async def read_root():
    return {"message": "Welcome to my retail shop"}


# List all products
@app.get("/products")
async def list_products(category: str = None, limit: int = 10):
    products = list(fake_db.values())

    # filter by category if provided
    if category:
        products = [p for p in products if p["category"] == category]

    return products[:limit]


# Featured — must be above /{product_id}
@app.get("/products/featured")
async def get_featured():
    return {"message": "These are featured products"}


# Get single product
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_db[product_id]


# Create product
@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    global next_id
    fake_db[next_id] = product.dict()
    created = {"id": next_id, **product.dict()}
    next_id += 1
    return created


# Update product
@app.put("/products/{id}")
async def update_product(id: int, product: Product):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    fake_db[id] = product.dict()
    return {"message": "Product updated", "id": id, "product": product}


# Delete product
@app.delete("/products/{id}")
async def delete_product(id: int):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = fake_db.pop(id)
    return {"message": "Product deleted", "deleted": deleted}


@app.get("/external-test")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()
    