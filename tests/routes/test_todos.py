from tests.factories import TodoFactory
from tests.factories import TodoState


def test_GET_todos_should_return_200(client, user, session, headers_token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get("/todos/", headers=headers_token)

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 5


def test_GET_todos_pagination_should_return_200(client, user, session, headers_token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get("/todos/?offset=1&limit=2", headers=headers_token)

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 2


# TESTES COPIADOS


def test_GET_todos_filter_by_tiltle(session, user, client, headers_token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1"))
    session.commit()

    response = client.get("/todos/?title=Test todo 1", headers=headers_token)

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 5


def test_GET_todos_filter_by_description(session, user, client, headers_token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, description="description"))
    session.commit()

    response = client.get("/todos/?description=desc", headers=headers_token)

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 5


def test_GET_todos_filter_by_state(session, user, client, headers_token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    session.commit()

    response = client.get("/todos/?state=draft", headers=headers_token)

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 5


def test_GET_todos_filter_combined(session, user, client, headers_token):
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5, user_id=user.id, title="Test todo combined", description="combined description", state=TodoState.done
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
        headers=headers_token,
    )

    assert response.status_code == 200
    assert len(response.json()["todos"]) == 5


def test_PATCH_todo_404_not_found(client, headers_token):
    response = client.patch("/todos/10", json={}, headers=headers_token)

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found."}


def test_PATCH_todo_200_OK(session, client, user, headers_token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(f"/todos/{todo.id}", json={"title": "teste!"}, headers=headers_token)
    assert response.status_code == 200
    assert response.json()["title"] == "teste!"


def test_DELETE_todo_200_OK(session, client, user, headers_token):
    todo = TodoFactory(id=1, user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(f"/todos/{todo.id}", headers=headers_token)

    assert response.status_code == 200
    assert response.json() == {"detail": "Task has been deleted successfully."}


def test_DELETE_todo_404_not_found(client, headers_token):
    response = client.delete(f"/todos/{10}", headers=headers_token)

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found."}
