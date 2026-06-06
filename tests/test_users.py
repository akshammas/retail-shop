# tests/test_users.py


def test_get_my_profile(client, customer_token):
    response = client.get(
        "/users/me/profile",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "customer@test.com"
    assert "password" not in data


def test_get_my_profile_no_token(client):
    response = client.get("/users/me/profile")
    assert response.status_code == 401


def test_update_name(client, customer_token):
    response = client.put(
        "/users/me/update",
        json={"name": "Updated Name"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_email(client, customer_token):
    response = client.put(
        "/users/me/update",
        json={"email": "newemail@test.com"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newemail@test.com"


def test_update_email_already_taken(client, customer_token, admin_token):
    # admin email is admin@test.com
    # try to update customer email to admin's email
    response = client.put(
        "/users/me/update",
        json={"email": "admin@test.com"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already in use"


def test_delete_own_account(client, customer_token):
    response = client.delete(
        "/users/me/delete",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()


def test_list_users_as_admin(client, admin_token, customer_token):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_users_as_customer(client, customer_token):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403


def test_admin_delete_user(client, admin_token, customer_token):
    # get customer id first
    profile = client.get(
        "/users/me/profile",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    customer_id = profile.json()["id"]

    # admin deletes customer
    response = client.delete(
        f"/users/{customer_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()


def test_get_user_not_found(client, admin_token):
    response = client.get(
        "/users/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404