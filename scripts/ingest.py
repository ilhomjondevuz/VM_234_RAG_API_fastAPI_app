import json
from pathlib import Path

import ollama

from app.infrastructure.chroma import get_collection


BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_PATH = (
    BASE_DIR
    / "data"
    / "documents"
    / "qaror_234"
    / "chunks.json"
)

EMBEDDING_MODEL = "nomic-embed-text:latest"


def load_chunks() -> list[dict]:
    """chunks.json faylini o'qiydi."""

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_embedding(text: str) -> list[float]:
    """Matn uchun embedding vector yaratadi."""

    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text,
    )

    return response["embedding"]


def ingest():
    """Chunklarni embedding qilib ChromaDB'ga yuklaydi."""

    chunks = load_chunks()

    collection = get_collection()

    print(f"Jami chunklar: {len(chunks)}")

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for index, chunk in enumerate(chunks):
        text = chunk["text"]

        print(
            f"Embedding yaratilmoqda: "
            f"{index + 1}/{len(chunks)}"
        )

        embedding = create_embedding(text)

        documents.append(text)
        embeddings.append(embedding)

        metadata = chunk.get("metadata", {})
        metadatas.append(metadata)

        ids.append(f"qaror_234_chunk_{index}")

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print()
    print("Embeddinglar ChromaDB'ga saqlandi.")
    print(f"Collection: {collection.name}")
    print(f"Jami saqlangan chunklar: {collection.count()}")


if __name__ == "__main__":
    ingest()