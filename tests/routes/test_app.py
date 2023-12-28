from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_PING_should_return_200_success(client):
    response = client.get("/ping/")

    assert response.status_code == 200
    assert response.json() == {"detail": "Pong"}
