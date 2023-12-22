from fastapi.testclient import TestClient

from app.app import app
from app.schemas import UserPublicDto

client = TestClient(app)


def test_GET_should_return_200_success(client, user):
    user_schema = UserPublicDto.model_validate(user).model_dump()
    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == {"users": [user_schema]}


def test_POST_should_return_400_already_registered(client, user):
    response = client.post("/users/", json={"username": "Test", "email": "gabriel@gmail.com", "password": "password"})

    assert response.status_code == 400
    assert {"detail": "Username already registered"}


def test_POST_should_return_201_success(client):
    response = client.post(
        "/users/", json={"username": "gabriel", "email": "gabriel@gmail.com", "password": "password"}
    )
    assert response.status_code == 201
    assert response.json() == {"username": "gabriel", "email": "gabriel@gmail.com", "id": 1}


def test_PUT_should_return_200_success(client, user):
    response = client.put(
        "/users/1", json={"username": "Pedro", "email": "pedro@gmail.com", "password": "new_password"}
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "Pedro", "email": "pedro@gmail.com"}


def test_PUT_should_return_404_failed(client, user):
    response = client.put(
        "/users/0", json={"username": "Pedro", "email": "pedro@gmail.com", "password": "new_password"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


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


def test_DELETE_should_return_404_failed(client, user):
    response = client.delete("/users/2")

    response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_DELETE_should_return_200_OK_success(client, user):
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token