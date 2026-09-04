from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import settings


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_PERSIST_DIRECTORY = (
    BASE_DIR / settings.chroma_persist_directory
)


def get_chroma_client():
    """
    Persistent ChromaDB client yaratadi.
    Ma'lumotlar data/chroma/ ichida saqlanadi.
    """

    CHROMA_PERSIST_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    return chromadb.PersistentClient(
        path=str(CHROMA_PERSIST_DIRECTORY)
    )


def get_collection() -> Collection:
    """
    234-son qaror uchun ChromaDB collection'ni
    yaratadi yoki mavjud collection'ni qaytaradi.
    """

    client = get_chroma_client()

    return client.get_or_create_collection(
        name=settings.chroma_collection_name,
        metadata={
            "description": (
                "O'zbekiston Respublikasi "
                "Vazirlar Mahkamasining 234-son qarori"
            )
        },
    )