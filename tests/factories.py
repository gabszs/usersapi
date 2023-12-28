import factory
from factory import Faker
from factory import fuzzy

from app.models import User
from app.models.models import Todo
from app.schemas.todo_schemas import TodoState


def factory_object_to_dict(factory_instance):
    """
    Converte um objeto criado por uma fábrica Factory Boy em um dicionário.

    Args:
        factory_instance: Objeto criado por uma fábrica Factory Boy.

    Returns:
        dict: Dicionário contendo os atributos do objeto.
    """
    attributes = factory_instance.__dict__
    # Remova atributos internos que não são relevantes para o dicionário
    attributes.pop("_declarations", None)
    return attributes


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda x: x)
    username = factory.LazyAttribute(lambda obj: f"test{obj.id}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = Faker("text")
    description = Faker("text")
    state = fuzzy.FuzzyChoice(TodoState)
    user_id = 1
