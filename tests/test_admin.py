# tests/test_admin.py


def test_admin_stats(client, admin_token):
    response = client.get(
        "/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_products" in data
    assert "total_users" in data
    assert "total_orders" in data
    assert "requested_by" in data
    assert data["requested_by"] == "admin@test.com"


def test_admin_stats_as_customer(client, customer_token):
    response = client.get(
        "/admin/stats",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_admin_stats_without_token(client):
    response = client.get("/admin/stats")
    assert response.status_code == 401


def test_admin_stats_user_count(client, admin_token, customer_token):
    # 2 users created by fixtures — admin and customer
    response = client.get(
        "/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["total_users"] == 2


def test_admin_stats_product_count(client, admin_token):
    response = client.get(
        "/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["total_products"] == 3