# tests/test_products.py


def test_list_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_products_filter_category(client):
    response = client.get("/products/?category=general")
    assert response.status_code == 200
    data = response.json()
    assert all(p["category"] == "general" for p in data)


def test_list_products_search(client):
    response = client.get("/products/?search=shirt")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("shirt" in p["name"].lower() for p in data)


def test_list_products_in_stock_filter(client):
    response = client.get("/products/?in_stock=true")
    assert response.status_code == 200
    data = response.json()
    assert all(p["in_stock"] for p in data)


def test_get_single_product(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "T-shirt"


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_featured_products(client):
    response = client.get("/products/featured")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product_as_admin(client, admin_token):
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
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jacket"
    assert "id" in data


def test_create_product_as_customer(client, customer_token):
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
    assert response.status_code == 403


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


def test_update_product_as_admin(client, admin_token):
    response = client.put(
        "/products/1",
        json={"name": "Updated T-shirt", "price": 599.99},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated T-shirt"
    assert data["price"] == 599.99


def test_update_product_as_customer(client, customer_token):
    response = client.put(
        "/products/1",
        json={"name": "Updated T-shirt"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403


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


def test_pagination(client):
    response = client.get("/products/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_pagination_limit_exceeded(client):
    response = client.get("/products/?limit=200")
    assert response.status_code == 400
    assert "Limit cannot exceed 100" in response.json()["detail"]


def test_admin_view_all_products(client, admin_token):
    response = client.get(
        "/products/admin/all",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product_invalid_price(client, admin_token):
    response = client.post(
        "/products/",
        json={
            "name": "Jacket",
            "price": -100,
            "description": "Winter jacket",
            "in_stock": True,
            "quantity": 15,
            "category": "outerwear"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422


# tests/test_products.py — add these


def test_search_no_results(client):
    response = client.get("/products/?search=xyznotexist")
    assert response.status_code == 200
    assert response.json() == []


def test_update_product_not_found(client, admin_token):
    response = client.put(
        "/products/999",
        json={"name": "Ghost Product"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product_not_found(client, admin_token):
    response = client.delete(
        "/products/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404


def test_create_product_missing_required_fields(client, admin_token):
    # missing name and price
    response = client.post(
        "/products/",
        json={
            "description": "No name or price"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422


def test_partial_update_only_price(client, admin_token):
    # update only price — name should stay the same
    response = client.put(
        "/products/1",
        json={"price": 299.99},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 299.99
    assert data["name"] == "T-shirt"  # unchanged


def test_partial_update_only_stock(client, admin_token):
    response = client.put(
        "/products/1",
        json={"in_stock": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["in_stock"] == False


def test_filter_out_of_stock(client, admin_token):
    # first mark product 1 as out of stock
    client.put(
        "/products/1",
        json={"in_stock": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    # filter in_stock=false
    response = client.get("/products/?in_stock=false")
    assert response.status_code == 200
    data = response.json()
    assert all(p["in_stock"] == False for p in data)


def test_admin_all_includes_out_of_stock(client, admin_token):
    # mark one as out of stock
    client.put(
        "/products/1",
        json={"in_stock": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    # admin all should still show it
    response = client.get(
        "/products/admin/all",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    ids = [p["id"] for p in response.json()]
    assert 1 in ids


def test_admin_all_as_customer(client, customer_token):
    response = client.get(
        "/products/admin/all",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403