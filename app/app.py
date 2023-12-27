from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import Message
from app.schemas import Token
from app.schemas import UserList
from app.schemas import UserPublicDto
from app.schemas import UserSchema
from app.security import create_access_token
from app.security import get_password_hash
from app.security import verify_password, get_current_user

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


@app.get("/users/", response_model=UserList)
def get_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {"users": users}


@app.post("/users/", status_code=201, response_model=UserPublicDto)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.username == user.username))

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put("/users/{id}", response_model=UserPublicDto)
def update_user(id: int, user: UserSchema, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user
    #
    # user_with_id = UserDB(**user.model_dump(), id=id)
    # database[id - 1] = user_with_id
    #
    # return user_with_id


@app.delete("/users/{id}", response_model=Message)
def delete_user(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(current_user)
    session.commit()

    return Message(detail="User deleted")


# Security


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)