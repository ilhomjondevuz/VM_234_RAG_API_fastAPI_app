import unicodedata
from pathlib import Path
import fitz

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data" / "documents" / "qaror_234" / "source.pdf"
OUTPUT_PATH = BASE_DIR / "data" / "documents" / "qaror_234" / "qaror_234.txt"


def clean_text(text: str) -> str:
    cleaned = []

    for ch in text:
        category = unicodedata.category(ch)

        # \n va \t ni saqlaymiz
        if ch in "\n\t":
            cleaned.append(ch)
            continue

        # Control belgilarni olib tashlaymiz
        if category.startswith("C"):
            continue

        # Symbol belgilarni olib tashlaymiz
        if category == "So":
            continue

        cleaned.append(ch)

    return "".join(cleaned)


def extract_text():
    document = fitz.open(PDF_PATH)

    text_parts = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        if text.strip():
            text_parts.append(
                f"\n--- SAHIFA {page_number} ---\n"
                f"{text}"
            )

    document.close()

    full_text = "\n".join(text_parts)

    full_text = clean_text(full_text)

    OUTPUT_PATH.write_text(
        full_text,
        encoding="utf-8"
    )

    print(f"Text saqlandi: {OUTPUT_PATH}")
    print(f"Belgilar soni: {len(full_text)}")


if __name__ == "__main__":
    extract_text()