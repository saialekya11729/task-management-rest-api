import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import User


@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def create_user(username="testuser", email="test@example.com", password="password123", role="user"):
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email="test@example.com", password="password123"):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    return response.get_json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}
