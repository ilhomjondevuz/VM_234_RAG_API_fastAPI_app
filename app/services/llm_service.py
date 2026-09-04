from app.infrastructure.ollama import generate_answer


def generate_rag_answer(prompt: str) -> str:
    """
    RAG prompt asosida LLM javobini yaratadi.
    """

    return generate_answer(prompt)