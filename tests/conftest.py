# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import fake_users_db, fake_products_db


@pytest.fixture
def client():
    """Fresh test client for each test"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_databases():
    """Reset fake databases before each test"""
    # clear users
    fake_users_db.clear()

    # reset products to original state
    fake_products_db.clear()
    fake_products_db.update({
        1: {"id": 1, "name": "T-shirt", "price": 499.99, "quantity": 10, "category": "general", "description": "Cotton round neck", "in_stock": True},
        2: {"id": 2, "name": "Shirt", "price": 999.99, "quantity": 5, "category": "general", "description": "Formal shirt", "in_stock": True},
        3: {"id": 3, "name": "Shorts", "price": 299.99, "quantity": 20, "category": "general", "description": "Sports shorts", "in_stock": True},
    })

    yield  # test runs here

    # cleanup after test
    fake_users_db.clear()


@pytest.fixture
def customer_token(client):
    """Create a customer and return their token"""
    response = client.post("/auth/signup", json={
        "name": "Test Customer",
        "email": "customer@test.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client):
    """Create an admin and return their token"""
    response = client.post("/auth/signup-admin", json={
        "name": "Test Admin",
        "email": "admin@test.com",
        "password": "adminpass123"
    })
    return response.json()["access_token"]