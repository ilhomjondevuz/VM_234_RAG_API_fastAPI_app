from app.promts.rag_promt import build_rag_prompt
from app.services.llm_service import generate_rag_answer
from app.services.retrieval_service import retrieve_relevant_chunks


def answer_question(question: str) -> dict:
    """
    To'liq RAG pipeline:

    question
       ↓
    retrieval
       ↓
    context
       ↓
    prompt
       ↓
    LLM
       ↓
    answer
    """

    chunks = retrieve_relevant_chunks(question)

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Manba {index}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    answer = generate_rag_answer(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources": chunks,
    }