from tests.conftest import auth_header


def test_user_can_register_login_and_view_profile(client):
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "alex",
            "email": "alex@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201
    assert register_response.get_json()["user"]["email"] == "alex@example.com"

    login_response = client.post(
        "/api/auth/login",
        json={"email": "alex@example.com", "password": "password123"},
    )

    assert login_response.status_code == 200
    token = login_response.get_json()["access_token"]

    me_response = client.get("/api/auth/me", headers=auth_header(token))

    assert me_response.status_code == 200
    assert me_response.get_json()["user"]["username"] == "alex"


def test_login_rejects_bad_password(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "alex",
            "email": "alex@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "alex@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_protected_routes_require_jwt(client):
    response = client.get("/api/tasks")

    assert response.status_code == 401
