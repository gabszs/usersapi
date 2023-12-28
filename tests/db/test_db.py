import pytest
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.models.models import Todo


def test_create_todo(session, user):
    todo = Todo(title="Test Todo", description="Test Desc", state="draft", user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos


def test_get_session():
    with pytest.MonkeyPatch.context() as env_mock:
        env_mock.setenv("DATABASE_URL", "sqlite:///:memory:")

        session_generator = get_session()

        session_instance = next(session_generator, None)
        assert isinstance(session_instance, Session)

        result = session_instance.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_create_user_success(session):
    new_user = User(username="Gabriel", password="password", email="gabrielizaac2020@gmail.com")

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == "Gabriel"))

    assert user.username == "Gabriel"
    assert user.password == "password"
    assert user.email == "gabrielizaac2020@gmail.com"
