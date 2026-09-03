from pathlib import Path
import json
import re


BASE_PATH = Path(__file__).parent.parent

INPUT_PATH = (
    BASE_PATH
    / "data"
    / "documents"
    / "qaror_234"
    / "qaror_234.txt"
)

OUTPUT_PATH = (
    BASE_PATH
    / "data"
    / "documents"
    / "qaror_234"
    / "chunks.json"
)


# Har bir chunk maksimal 1000 ta belgi
CHUNK_SIZE = 1000

# Keyingi chunk oldingisidan 150 ta belgini takror oladi
CHUNK_OVERLAP = 150


def split_long_paragraph(paragraph: str):
    """
    Juda uzun paragraphni CHUNK_SIZE dan oshmaydigan
    kichik qismlarga bo'ladi.
    """

    parts = []

    start = 0

    while start < len(paragraph):
        end = start + CHUNK_SIZE

        part = paragraph[start:end].strip()

        if part:
            parts.append(part)

        # Keyingi qism oldingi qismning
        # CHUNK_OVERLAP ta belgisini takrorlaydi.
        start = end - CHUNK_OVERLAP

    return parts


def split_text(text: str):
    paragraphs = re.split(r"\n\s*\n", text)

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Agar paragraphning o'zi juda uzun bo'lsa,
        # uni avval kichik qismlarga bo'lamiz.
        if len(paragraph) > CHUNK_SIZE:

            # Hozirgi chunkni saqlaymiz
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # Uzun paragraphni bo'lib qo'shamiz
            long_parts = split_long_paragraph(paragraph)

            chunks.extend(long_parts)

            continue

        # Oddiy paragraph
        if len(current_chunk) + len(paragraph) + 2 <= CHUNK_SIZE:
            current_chunk += paragraph + "\n\n"

        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            overlap = current_chunk[-CHUNK_OVERLAP:]

            current_chunk = overlap + "\n\n" + paragraph

    # Oxirgi chunk
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
                    "document": (
                        "Vazirlar Mahkamasining "
                        "234-son qarori"
                    ),
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

    print(f"Maksimal chunk uzunligi: {max(map(lambda x: len(x['text']), result))}")

    print(f"Fayl saqlandi: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_chunks()