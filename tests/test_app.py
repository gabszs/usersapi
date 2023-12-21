from fastapi.testclient import TestClient

from app.app import app


client = TestClient(app)


def test_GET_should_return_200_success_hello_world(client):
    response = client.get("/users/")

    assert response.status_code == 200
    # assert response.json() == {"users": "Hello World!!"}


def test_POST_should_return_201_success(client):
    # response = client.put(
    #     '/users/1',
    #     json={
    #         'username': 'bob',
    #         'email': 'bob@example.com',
    #         'password': 'mynewpassword',
    #     },
    # )
    # assert response.status_code == 200
    # assert response.json() == {
    #     'username': 'bob',
    #     'email': 'bob@example.com',
    #     'id': 1,
    # }
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_PUT_should_return_200_success(client):
    response = client.put(
        "/users/1", json={"username": "Pedro", "email": "pedro@gmail.com", "password": "new_password"}
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "Pedro", "email": "pedro@gmail.com"}


def test_PUT_should_return_404_failed(client):
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


def test_DELETE_should_return_404_failed(client):
    response = client.delete("/users/2")

    response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_DELETE_should_return_200_OK_success(client):
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}
