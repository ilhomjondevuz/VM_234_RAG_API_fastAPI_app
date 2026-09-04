from fastapi import APIRouter

from app.schemas.schema import ChatRequest, ChatResponse
from app.services.rag_sevice import answer_question


chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chat_router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):
    """
    234-son qarori asosida savolga javob beradi.
    """

    return answer_question(request.question)