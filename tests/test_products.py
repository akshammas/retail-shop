# tests/test_products.py


def test_list_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # 3 products in fake db


def test_get_single_product(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "T-shirt"
    assert data["id"] == 1


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_create_product_with_token(client, customer_token):
    response = client.post(
        "/products/",
        json={
            "name": "Jacket",
            "price": 1499.99,
            "description": "Winter jacket",
            "in_stock": True,
            "quantity": 15,
            "category": "outerwear"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jacket"
    assert data["price"] == 1499.99
    assert "id" in data


def test_create_product_without_token(client):
    response = client.post(
        "/products/",
        json={
            "name": "Jacket",
            "price": 1499.99,
            "description": "Winter jacket",
            "in_stock": True,
            "quantity": 15,
            "category": "outerwear"
        }
    )
    assert response.status_code == 401


def test_create_product_invalid_price(client, customer_token):
    response = client.post(
        "/products/",
        json={
            "name": "Jacket",
            "price": -100,  # invalid price
            "description": "Winter jacket",
            "in_stock": True,
            "quantity": 15,
            "category": "outerwear"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 422  # pydantic validation error


def test_delete_product_as_admin(client, admin_token):
    response = client.delete(
        "/products/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted"


def test_delete_product_as_customer(client, customer_token):
    response = client.delete(
        "/products/1",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_pagination(client):
    response = client.get("/products/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_pagination_limit_exceeded(client):
    response = client.get("/products/?limit=200")
    assert response.status_code == 400
    assert "Limit cannot exceed 100" in response.json()["detail"]