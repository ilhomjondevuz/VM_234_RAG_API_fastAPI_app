from app.services import retrieval_service


def test_retrieve_relevant_chunks(monkeypatch):
    fake_embedding = [0.1, 0.2, 0.3]

    class FakeCollection:
        def query(self, **kwargs):
            assert kwargs["query_embeddings"] == [fake_embedding]
            assert kwargs["n_results"] == 2

            return {
                "documents": [
                    [
                        "234-son qarorning birinchi relevant qismi.",
                        "234-son qarorning ikkinchi relevant qismi.",
                    ]
                ],
                "metadatas": [
                    [
                        {"page": 1, "chunk_id": 1},
                        {"page": 2, "chunk_id": 2},
                    ]
                ],
                "distances": [
                    [
                        0.10,
                        0.20,
                    ]
                ],
            }

    monkeypatch.setattr(
        retrieval_service,
        "get_collection",
        lambda: FakeCollection(),
    )

    monkeypatch.setattr(
        retrieval_service,
        "embed_text",
        lambda question: fake_embedding,
    )

    chunks = retrieval_service.retrieve_relevant_chunks(
        "234-son qaror nima haqida?",
        top_k=2,
    )

    assert len(chunks) == 2

    assert chunks[0]["text"] == (
        "234-son qarorning birinchi relevant qismi."
    )

    assert chunks[0]["metadata"]["page"] == 1
    assert chunks[0]["distance"] == 0.10

    assert chunks[1]["metadata"]["chunk_id"] == 2