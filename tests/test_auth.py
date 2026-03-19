import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import engine, SessionLocal, Base
from backend.models.user import User
import bcrypt


@pytest.fixture
def client(db_session):
    yield TestClient(app)


@pytest.fixture
def test_user(db_session):
    from backend.models.video import Video
    from backend.models.script import Script
    password_hash = bcrypt.hashpw("testpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(username="testuser", password_hash=password_hash, role="user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_login_success(client, test_user):
    response = client.post("/api/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user"]["username"] == "testuser"


def test_login_fail_wrong_password(client, test_user):
    response = client.post("/api/login", json={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401


def test_get_current_user(client, test_user):
    from requests.auth import HTTPBasicAuth
    response = client.get("/api/me", auth=HTTPBasicAuth("testuser", "testpass"))
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_get_current_user_unauthorized(client, test_user):
    from requests.auth import HTTPBasicAuth
    response = client.get("/api/me", auth=HTTPBasicAuth("testuser", "wrongpass"))
    assert response.status_code == 401


def test_login_empty_username(client, test_user):
    response = client.post("/api/login", json={"username": "", "password": "testpass"})
    assert response.status_code == 401


def test_login_empty_password(client, test_user):
    response = client.post("/api/login", json={"username": "testuser", "password": ""})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/api/login", json={"username": "nonexistent", "password": "testpass"})
    assert response.status_code == 401


def test_login_very_long_username(client, test_user):
    long_username = "a" * 150
    response = client.post("/api/login", json={"username": long_username, "password": "testpass"})
    assert response.status_code == 401


def test_login_very_long_password(client, test_user):
    long_password = "p" * 150
    response = client.post("/api/login", json={"username": "testuser", "password": long_password})
    assert response.status_code == 401
