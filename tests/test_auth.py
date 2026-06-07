# tests/test_auth.py


def test_signup_success(client):
    response = client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "john@example.com"
    assert data["user"]["role"] == "customer"
    assert "password" not in data["user"]  # password never returned


def test_signup_duplicate_email(client):
    # signup once
    client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    # signup again with same email
    response = client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client):
    # signup first
    client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    # then login
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_wrong_email(client):
    response = client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "password123"
    })
    assert response.status_code == 401


def test_get_me_with_token(client, customer_token):
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "customer@test.com"
    assert "password" not in data


def test_get_me_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_refresh_token(client):
    signup = client.post("/auth/signup", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    })
    refresh_token = signup.json()["refresh_token"]

    response = client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_logout(client, customer_token):
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    assert "logged out" in response.json()["message"].lower()



def test_signup_admin_success(client):
    response = client.post("/auth/signup-admin", json={
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "admin"
    assert "access_token" in data


def test_signup_missing_fields(client):
    # missing password
    response = client.post("/auth/signup", json={
        "name": "John",
        "email": "john@example.com"
    })
    assert response.status_code == 422


def test_signup_empty_body(client):
    response = client.post("/auth/signup", json={})
    assert response.status_code == 422


def test_login_missing_fields(client):
    response = client.post("/auth/login", json={
        "email": "john@example.com"
        # missing password
    })
    assert response.status_code == 422


def test_refresh_with_invalid_token(client):
    response = client.post("/auth/refresh", json={
        "refresh_token": "this.is.fake"
    })
    assert response.status_code == 401


def test_refresh_with_access_token_instead(client):
    # signup and use access token as refresh token
    signup = client.post("/auth/signup", json={
        "name": "John",
        "email": "john@example.com",
        "password": "password123"
    })
    access_token = signup.json()["access_token"]

    response = client.post("/auth/refresh", json={
        "refresh_token": access_token  # wrong token type
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token type"


def test_profile_returns_welcome_message(client, customer_token):
    response = client.get(
        "/auth/profile",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome back" in response.json()["message"]


def test_logout_without_token(client):
    response = client.post("/auth/logout")
    assert response.status_code == 401