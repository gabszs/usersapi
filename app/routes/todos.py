from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.models.models import Todo
from app.schemas.todo_schemas import TodoList
from app.schemas.todo_schemas import TodoPublic
from app.schemas.todo_schemas import TodoSchema
from app.security import get_current_user

CurrentUser = Annotated[User, Depends(get_current_user)]
Sessions = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=TodoList)
def list_todos(
    session: Sessions,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {"todos": todos}


@router.post("/", response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: Sessions):
    db_todo: Todo = Todo(title=todo.title, description=todo.description, state=todo.state, user_id=user.id)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
