from sqlalchemy import select

from app.models import User


def test_create_user_success(session):
    new_user = User(username="Gabriel", password="password", email="gabrielizaac2020@gmail.com")

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == "Gabriel"))

    assert user.username == "Gabriel"
    assert user.password == "password"
    assert user.email == "gabrielizaac2020@gmail.com"
