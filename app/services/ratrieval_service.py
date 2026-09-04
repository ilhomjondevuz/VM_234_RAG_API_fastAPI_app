from app.core.config import settings
from app.infrastructure.chroma import get_collection
from app.services.embedding_service import embed_text


def retrieve_relevant_chunks(
    question: str,
    top_k: int | None = None,
) -> list[dict]:
    """
    Foydalanuvchi savoliga eng mos chunklarni
    ChromaDB'dan topadi.
    """

    collection = get_collection()

    question_embedding = embed_text(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k or settings.retrieval_top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return chunks