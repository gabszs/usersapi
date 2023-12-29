from fastapi.testclient import TestClient

from app.app import app
from app.schemas.users_schema import UserPublicDto

client = TestClient(app)


def test_GET_should_return_200_success(client, user):
    user_schema = UserPublicDto.model_validate(user).model_dump()
    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == {"users": [user_schema]}


def test_POST_should_return_409_already_registered(client, user):
    response = client.post(
        "/users/", json={"username": user.username, "email": user.email, "password": user.clean_password}
    )

    assert response.status_code == 409
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


def test_PUT_should_return_200_success(client, user, headers_token):
    response = client.put(
        f"/users/{user.id}",
        headers=headers_token,
        json={"username": "Pedro", "email": "pedro@gmail.com", "password": user.clean_password},
    )

    assert response.status_code == 200
    assert response.json() == {"id": user.id, "username": "Pedro", "email": "pedro@gmail.com"}


def test_PUT_should_return_401_unauthorized(client, user, headers_token):
    response = client.put(
        "/users/0",
        headers=headers_token,
        json={"username": "Pedro", "email": "pedro@gmail.com", "password": "new_password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not enough permissions"}


def test_PUT_should_return_409_conflict(client, user, other_user, headers_token):
    response = client.put(
        f"/users/{user.id}",
        headers=headers_token,
        json={"username": other_user.username, "email": user.email, "password": user.clean_password},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Username already registered"}


def test_DELETE_should_return_404_failed(client, user, headers_token):
    response = client.delete("/users/2", headers=headers_token)

    response.status_code == 400
    assert response.json() == {"detail": "Not enough permissions"}


def test_DELETE_should_return_200_OK_success(client, user, headers_token):
    response = client.delete(f"/users/{user.id}", headers=headers_token)

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_DELETE_should_return_401_with_wrong_user(client, other_user, headers_token):
    response = client.delete(f"/users/{other_user.id}", headers=headers_token)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not enough permissions"}
