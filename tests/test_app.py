from fastapi.testclient import TestClient
from app.app import app


client = TestClient(app)


def test_root_should_return_200OK_hello_world():
    client = TestClient(app)
    
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World!!"}