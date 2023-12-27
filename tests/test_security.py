
from jose import jwt
from app.security import create_access_token, SECRET_KEY


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']

def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token

# def test_jwt_create_access_token():
#     data = {"test": "test"}
#     token = create_access_token(data)

#     decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

#     assert decoded["test"] == data["test"]
#     assert decoded["exp"]


# def test_get_password_hash_function():
#     password = "password_test"
#     hashed_password = get_password_hash(password)

#     assert password != hashed_password



