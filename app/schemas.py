from typing import List

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicDto(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: List[UserPublicDto]


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str
