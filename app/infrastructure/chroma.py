from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_PERSIST_DIRECTORY = (
    BASE_DIR / "data" / "chroma"
)

COLLECTION_NAME = "vm_234_qaror"


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
        name=COLLECTION_NAME,
        metadata={
            "description": (
                "O'zbekiston Respublikasi "
                "Vazirlar Mahkamasining 234-son qarori"
            )
        },
    )