from pathlib import Path
import json
import re


BASE_PATH = Path(__file__).parent.parent
INPUT_PATH = BASE_PATH / "data" / "documents" / "qaror_234" / "qaror_234.txt"
OUTPUT_PATH = BASE_PATH / "data" / "documents" / "qaror_234" / "chunks.json"

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200


def split_text(text: str):
    paragraphs = re.split(r"\n\s*\n", text)

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) <= CHUNK_SIZE:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            overlap = current_chunk[-CHUNK_OVERLAP:]

            current_chunk = overlap + "\n\n" + paragraph

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def create_chunks():
    text = INPUT_PATH.read_text(encoding="utf-8")

    chunks = split_text(text)

    result = []

    for index, chunk in enumerate(chunks):
        result.append(
            {
                "id": f"qaror_234_{index}",
                "text": chunk,
                "metadata": {
                    "document": "Vazirlar Mahkamasining 234-son qarori",
                    "source": "source.pdf",
                    "chunk_index": index,
                },
            }
        )

    OUTPUT_PATH.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"Chunklar soni: {len(result)}")
    print(f"Fayl saqlandi: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_chunks()