from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import chat


client = TestClient(app)


def test_chat():
    def fake_answer_question(question: str) -> dict:
        return {
            "question": question,
            "answer": "234-son qaror asosida test javobi.",
            "sources": [
                {
                    "text": "Test uchun 234-son qarordan olingan matn.",
                    "metadata": {
                        "page": 1,
                        "chunk_id": 1,
                    },
                    "distance": 0.1,
                }
            ],
        }

    original = chat.answer_question
    chat.answer_question = fake_answer_question

    try:
        response = client.post(
            "/chat/",
            json={
                "question": "234-son qaror nima haqida?"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["question"] == "234-son qaror nima haqida?"
        assert data["answer"]
        assert isinstance(data["sources"], list)
        assert len(data["sources"]) > 0

    finally:
        chat.answer_question = original


def test_chat_invalid_question():
    response = client.post(
        "/chat/",
        json={
            "question": "a"
        },
    )

    assert response.status_code == 422