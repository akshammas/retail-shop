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



    # tests/test_users.py — add these


def test_update_password(client, customer_token):
    # update password
    response = client.put(
        "/users/me/update",
        json={"password": "newpassword456"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200

    # login with new password should work
    login = client.post("/auth/login", json={
        "email": "customer@test.com",
        "password": "newpassword456"
    })
    assert login.status_code == 200


def test_update_nothing_sent(client, customer_token):
    # send empty update — should still return 200
    response = client.put(
        "/users/me/update",
        json={},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200


def test_get_user_as_customer(client, customer_token):
    # customers cannot get other users by id
    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403


def test_admin_cannot_delete_themselves(client, admin_token):
    # get admin id
    me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    admin_id = me.json()["id"]

    # try to delete own account via admin route
    response = client.delete(
        f"/users/{admin_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert "Cannot delete your own account" in response.json()["detail"]


def test_delete_nonexistent_user(client, admin_token):
    response = client.delete(
        "/users/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404


def test_update_without_token(client):
    response = client.put(
        "/users/me/update",
        json={"name": "Hacker"}
    )
    assert response.status_code == 401


def test_delete_without_token(client):
    response = client.delete("/users/me/delete")
    assert response.status_code == 401