import json
from pathlib import Path

from app.infrastructure.chroma import get_collection
from app.infrastructure.ollama import create_embedding


BASE_DIR = Path(__file__).resolve().parents[1]

CHUNKS_PATH = (
    BASE_DIR
    / "data"
    / "documents"
    / "qaror_234"
    / "chunks.json"
)


def load_chunks() -> list[dict]:
    """
    chunks.json faylini o'qiydi.
    """

    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def ingest():
    """
    chunks.json dagi barcha chunklarni:

        text
          ↓
        embedding
          ↓
        ChromaDB

    ko'rinishida saqlaydi.
    """

    chunks = load_chunks()

    collection = get_collection()

    print(f"Jami chunklar: {len(chunks)}")
    print(f"Collection: {collection.name}")
    print()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        text = chunk["text"]

        print(
            f"[{index + 1}/{len(chunks)}] "
            f"Embedding yaratilmoqda..."
        )

        embedding = create_embedding(text)

        ids.append(
            f"qaror_234_chunk_{index}"
        )

        documents.append(text)

        embeddings.append(embedding)

        metadatas.append(
            chunk.get("metadata", {})
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print()
    print("================================")
    print("INGESTION YAKUNLANDI")
    print("================================")
    print(f"Collection: {collection.name}")
    print(f"Chunklar: {collection.count()}")


if __name__ == "__main__":
    ingest()