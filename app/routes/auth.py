from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas.token_schema import Token
from app.security import create_access_token
from app.security import get_current_user
from app.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2Form,
    session: Sessions,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh_token", response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={"sub": user.email})

    return {"access_token": new_access_token, "token_type": "bearer"}
