from app.infrastructure.ollama import create_embedding


def embed_text(text: str) -> list[float]:
    """
    Berilgan matn uchun embedding yaratadi.
    """

    return create_embedding(text)