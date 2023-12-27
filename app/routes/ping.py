from fastapi import APIRouter
from app.schemas import Message

router = APIRouter(prefix="/ping", tags=['ping'])

@router.get('/')
async def ping(response_model=Message):
    return Message(detail="Pong")