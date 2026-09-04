from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        description="234-son qarori bo'yicha foydalanuvchi savoli",
    )


class SourceChunk(BaseModel):
    text: str
    metadata: dict
    distance: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]