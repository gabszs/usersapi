from tests.factories import TodoFactory
from tests.factories import TodoState


def test_GET_todos_should_return_200(client, user, session, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get("/todos/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 5


def test_GET_todos_pagination_should_return_200(client, user, session, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get("/todos/?offset=1&limit=2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 2


# TESTES COPIADOS


def test_list_todos_filter_title(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1"))
    session.commit()

    response = client.get(
        "/todos/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == 5


def test_list_todos_filter_description(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, description="description"))
    session.commit()

    response = client.get(
        "/todos/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == 5


def test_list_todos_filter_state(session, user, client, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    session.commit()

    response = client.get(
        "/todos/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == 5


def test_list_todos_filter_combined(session, user, client, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title="Test todo combined",
            description="combined description",
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title="Other title",
            description="other description",
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        "/todos/?title=Test todo combined&description=combined&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == 5
