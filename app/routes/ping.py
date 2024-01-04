from fastapi import APIRouter

from app.schemas.base_schemas import Message

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/", response_model=Message)
async def ping():
    return Message(detail="Pong")
