import ollama

from app.core.config import settings


def create_embedding(text: str) -> list[float]:
    """
    Matn uchun Ollama embedding yaratadi.
    """

    response = ollama.embeddings(
        model=settings.embedding_model,
        prompt=text,
    )

    return response["embedding"]


def generate_answer(prompt: str) -> str:
    """
    Qwen orqali javob generatsiya qiladi.
    """

    response = ollama.chat(
        model=settings.ollama_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]