from fastapi.testclient import TestClient

from jwt_gen.jwtcreator import JwtCreator
from main import app


client = TestClient(app)


fake_token = JwtCreator(payload={
        'id': 'd5f8751e-397d-4879-8a51-1249e068ff9f',
        'user_name': 'jhon_doe',
        'password': 'pass',
        'request_limit': 10
    }).createToken()


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


def test_exchange_rates_invalid_token():
    response = client.put(
        "exchange/rates",
        headers={
            "authorization": "Bearer eyJ0eXAiOKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImI0MDk2ZGU5LTZhMTEtNDIzNS04Y2RkLTgwY2Y5NzFkZjM4NSIsInVzZXJfbmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJQQHNzVzByZCIsInJlcXVlc3RfbGltaXQiOjEwfQ.2wlOMrd1NBXK75JnNCJzOj1rmkNXWI0T28OYfzaQUr0"}
    )

    assert response.status_code == 406


def test_exchange_rates_invalid_bearer_token():
    response = client.put(
        "exchange/rates",
        headers={
            "authorization": "eyJ0eXAiOKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImI0MDk2ZGU5LTZhMTEtNDIzNS04Y2RkLTgwY2Y5NzFkZjM4NSIsInVzZXJfbmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJQQHNzVzByZCIsInJlcXVlc3RfbGltaXQiOjEwfQ.2wlOMrd1NBXK75JnNCJzOj1rmkNXWI0T28OYfzaQUr0"}
    )

    assert response.status_code == 406


def test_exchange_rates_invalid_auth():
    response = client.put(
        "exchange/rates"
    )

    assert response.status_code == 401


def test_exchange_rates_invalid_user():
    response = client.put(
        "exchange/rates",
        headers={"authorization": "Bearer " + fake_token}
    )

    assert response.status_code == 401


def test_exchange_rates():
    response = client.put(
        "exchange/rates",
        headers={"authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImI0MDk2ZGU5LTZhMTEtNDIzNS04Y2RkLTgwY2Y5NzFkZjM4NSIsInVzZXJfbmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJQQHNzVzByZCIsInJlcXVlc3RfbGltaXQiOjEwfQ.2wlOMrd1NBXK75JnNCJzOj1rmkNXWI0T28OYfzaQUr0"}
    )

    assert response.status_code == 200
