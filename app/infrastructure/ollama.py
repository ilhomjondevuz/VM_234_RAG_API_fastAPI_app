import ollama


EMBEDDING_MODEL = "nomic-embed-text:latest"
LLM_MODEL = "qwen2.5:7b"


def create_embedding(text: str) -> list[float]:
    """
    Matn uchun Ollama embedding yaratadi.
    """

    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text,
    )

    return response["embedding"]


def generate_answer(prompt: str) -> str:
    """
    Qwen orqali javob generatsiya qiladi.
    """

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]