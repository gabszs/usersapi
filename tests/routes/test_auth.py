from freezegun import freeze_time


def test_token_expired_after_time(client, user):
    with freeze_time("2023-12-28 12:00:00"):
        response = client.post("/auth/token", data={"username": user.email, "password": user.clean_password})

        assert response.status_code == 200
        token = response.json()["access_token"]

    with freeze_time("2023-12-28 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"username": "test", "email": "test@test.com", "password": "testword"},
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_inexistent_user(client):
    response = client.post("/auth/token", data={"username": "test@test.com", "password": "testword"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_wrong_password(client, user):
    response = client.post("/auth/token", data={"username": user.username, "password": "wrongpassword"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_wrong_email(client, user):
    response = client.post("/auth/token", data={"username": "wrong@password.com", "password": user.clean_password})

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


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

    assert request.status_code == 401
    assert request.json() == {"detail": "Incorrect email or password"}


def test_get_token_400_incorrect_username(client, user):
    request = client.post("auth/token/", data={"username": "wrong_user", "password": user.clean_password})

    assert request.status_code == 401
    assert request.json() == {"detail": "Incorrect email or password"}


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2023-12-28 12:00:00"):
        response = client.post("/auth/token", data={"username": user.email, "password": user.clean_password})

        assert response.status_code == 200
        token = response.json()["access_token"]

    with freeze_time("2023-12-28 12:31:00"):
        response = client.post("/auth/refresh_token", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_refresh_token(client, user, headers_token):
    response = client.post("/auth/refresh_token", headers=headers_token)
    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
