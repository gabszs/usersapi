from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas.base_schemas import Message
from app.schemas.users_schema import UserList
from app.schemas.users_schema import UserPublicDto
from app.schemas.users_schema import UserSchema
from app.security import get_current_user
from app.security import get_password_hash


router = APIRouter(prefix="/users", tags=["users"])

Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/", response_model=UserList)
def get_users(session: Sessions, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return UserList(users=users)


@router.post("/", status_code=201, response_model=UserPublicDto)
def create_user(user: UserSchema, session: Sessions):
    db_user = session.scalar(select(User).where(User.username == user.username))

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put("/{id}", response_model=UserPublicDto)
def update_user(id: int, user: UserSchema, session: Sessions, current_user: CurrentUser):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")

    user_exist = session.scalar(select(User).where(User.email == user.email))
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete("/{id}", response_model=Message)
def delete_user(id: int, session: Sessions, current_user: CurrentUser):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")

    session.delete(current_user)
    session.commit()

    return Message(detail="User deleted")
