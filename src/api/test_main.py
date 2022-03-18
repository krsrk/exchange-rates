from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_auth_endpoint():
    response = client.get("/auth")
    assert response.status_code == 200
    assert response.json() == {"message": "Auth Service"}


def test_auth_login_endpoint():
    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "P@ssW0rd"
        },
    )
    assert response.status_code == 200
