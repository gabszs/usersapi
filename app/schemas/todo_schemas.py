from pydantic import BaseModel

from app.models.models import TodoState


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    state: TodoState


class TodoList(BaseModel):
    todos: list[TodoPublic]
