# app/database.py

# Shared in-memory databases
# Phase 2 (Week 7) will replace these with real PostgreSQL tables

fake_users_db = {}

fake_products_db = {
    1: {
        "id": 1,
        "name": "T-shirt",
        "price": 499.99,
        "quantity": 10,
        "category": "general",
        "description": "Cotton round neck",
        "in_stock": True
    },
    2: {
        "id": 2,
        "name": "Shirt",
        "price": 999.99,
        "quantity": 5,
        "category": "general",
        "description": "Formal shirt",
        "in_stock": True
    },
    3: {
        "id": 3,
        "name": "Shorts",
        "price": 299.99,
        "quantity": 20,
        "category": "general",
        "description": "Sports shorts",
        "in_stock": True
    },
}