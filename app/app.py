from typing import List

from fastapi import FastAPI
from fastapi import HTTPException

from app.schemas import Message
from app.schemas import UserDB
from app.schemas import UserList
from app.schemas import UserPublicDto
from app.schemas import UserSchema

app = FastAPI(
    title="UsersApi",
    description="Users Web api with basic auth crud built by @BRDEV team",
    contact={
        "name": "Gabriel Carvalho",
        "url": "https://www.linkedin.com/in/gabzsz/",
        "email": "gabriel.carvalho@huawei.com",
    },
    summary="WebApi build on best market practices such as TDD, Clean Arch, Data Validation with Pydantic V2",
)

database: List[UserPublicDto] = []


@app.get("/users/", response_model=UserList)
def get_users():
    return {"users": database}


@app.post("/users/", status_code=201, response_model=UserPublicDto)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)
    return user_with_id


@app.put("/users/{id}", response_model=UserPublicDto)
def update_user(id: int, user: UserSchema):
    if id < 1 or id > len(database):
        raise HTTPException(status_code=404, detail="User not found")

    user_with_id = UserDB(**user.model_dump(), id=id)
    database[id - 1] = user_with_id

    return user_with_id


@app.delete("/users/{id}", response_model=Message)
def delete_user(id: int):
    if id > len(database) or id < 1:
        raise HTTPException(status_code=404, detail="User not found")

    del database[id - 1]

    return Message(detail="User deleted")


# @app.put('/users/{id}')
