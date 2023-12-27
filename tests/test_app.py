from fastapi.testclient import TestClient

from app.app import app
from app.schemas import UserPublicDto

client = TestClient(app)

def test_PING_should_return_200_success(client):
    response = client.get("/ping/")

    assert response.status_code == 200
    assert response.json() == {"detail": "Pong"}

def test_GET_should_return_200_success(client, user):
    user_schema = UserPublicDto.model_validate(user).model_dump()
    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == {"users": [user_schema]}


def test_POST_should_return_400_already_registered(client, user):
    response = client.post("/users/", json={"username": "Teste", "email": "teste@test.com", "password": "testtest"})

    assert response.status_code == 400
    assert {"detail": "Username already registered"}


def test_POST_should_return_201_success(client):
    response = client.post(
        "/users/", json={"username": "gabriel", "email": "gabriel@gmail.com", "password": "password"}
    )
    assert response.status_code == 201
    assert response.json() == {"username": "gabriel", "email": "gabriel@gmail.com", "id": 1}


def test_POST_should_return_422_Unprocessed_failed(client):
    response = client.post(
        "/users/",
        json={
            "username": "Gabriel",
            "email": "gabriel.carvalho@huawei.com",
            "password12": "secret_password",  # incorrect by purpose
        },
    )

    assert response.status_code == 422


def test_PUT_should_return_200_success(client, user, token):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Pedro", "email": "pedro@gmail.com", "password": user.clean_password},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "Pedro", "email": "pedro@gmail.com"}


def test_PUT_should_return_400_failed(client, user, token):
    response = client.put(
        "/users/0",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Pedro", "email": "pedro@gmail.com", "password": "new_password"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Not enough permissions"}


def test_DELETE_should_return_404_failed(client, user, token):
    response = client.delete("/users/2", headers={"Authorization": f"Bearer {token}"})

    response.status_code == 400
    assert response.json() == {"detail": "Not enough permissions"}


def test_DELETE_should_return_200_OK_success(client, user, token):
    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_get_route_without_token(client, user, token):
    response = client.delete("/users/1", headers={"Authorization": ""})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_token(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert "token_type" in token


def test_get_token_400_incorrect_password(client, user):
    request = client.post("auth/token/", data={"username": user.email, "password": "wrong_password"})

    assert request.status_code == 400
    assert request.json() == {"detail": "Incorrect email or password"}


def test_get_token_400_incorrect_username(client, user):
    request = client.post("auth/token/", data={"username": "wrong_user", "password": user.clean_password})

    assert request.status_code == 400
    assert request.json() == {"detail": "Incorrect email or password"}
