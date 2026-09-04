# VM 234 RAG API

Vazirlar Mahkamasining **2026-yil 11-maydagi 234-son qarori** matni asosida foydalanuvchi savollariga javob beruvchi **Retrieval-Augmented Generation (RAG)** API.

Loyiha foydalanuvchi savolini qabul qiladi, qaror matnidan unga eng mos bo‘lgan qismlarni topadi va topilgan ma'lumotlar asosida lokal LLM yordamida javob shakllantiradi.

Asosiy maqsad — modelning tashqi bilimlaridan foydalanmasdan, **faqat 234-son qaror matni asosida javob berish** va hallucination (uydirma javob) ehtimolini kamaytirish.

---

## 📌 Loyiha arxitekturasi

```text
                    Foydalanuvchi
                         │
                         ▼
                    FastAPI API
                         │
                         ▼
                      Savol
                         │
                         ▼
                Embedding Model
               nomic-embed-text
                         │
                         ▼
                    ChromaDB
                         │
                         │
             Relevant chunks topiladi
                         │
                         ▼
                  Context / Chunks
                         │
                         ▼
                  Ollama + Qwen
                         │
                         ▼
                       Javob
```

RAG pipeline:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
ChromaDB
   ↓
Relevant Chunks
   ↓
Prompt + Context
   ↓
Qwen
   ↓
Answer
```

---

# 🛠 Texnologiyalar

Loyiha quyidagi texnologiyalardan foydalanadi:

* Python 3.12+
* FastAPI
* Uvicorn
* Ollama
* Qwen 2.5 7B
* Nomic Embed Text
* ChromaDB
* PyMuPDF
* Pydantic
* python-dotenv
* pytest

---

# 📂 Loyiha strukturasi

```text
VM_234_RAG_API_fastAPI_app/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── schemas/
│   │   └── question.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   │   ├── llm_service.py
│   │   └── rag_service.py
│   │
│   └── infrastructure/
│       ├── ollama.py
│       └── chroma.py
│
├── data/
│   ├── documents/
│   │   └── qaror_234/
│   │       ├── source.pdf
│   │       ├── qaror_234.txt
│   │       └── chunks.json
│   │
│   └── chroma/
│
├── scripts/
│   ├── extract_text.py
│   ├── chunk_document.py
│   └── ingest.py
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# ⚙️ 1. Talablar

Loyihani ishga tushirishdan oldin kompyuterda quyidagilar bo‘lishi kerak:

* Python 3.12 yoki undan yuqori
* pip
* Git
* Ollama

Linux/Ubuntu uchun:

```bash
python3 --version
pip3 --version
git --version
ollama --version
```

Python versiyasi:

```text
Python 3.12+
```

bo‘lishi tavsiya qilinadi.

---

# 🐍 2. Repository'ni clone qilish

Repository:

```text
VM_234_RAG_API_fastAPI_app
```

Clone qilish:

```bash
git clone https://github.com/ilhomjondevuz/VM_234_RAG_API_fastAPI_app.git
```

Loyihaga kirish:

```bash
cd VM_234_RAG_API_fastAPI_app
```

---

# 🧪 3. Virtual environment yaratish

Linux/macOS:

```bash
python3 -m venv .venv
```

Virtual environment'ni ishga tushirish:

```bash
source .venv/bin/activate
```

Terminal boshida quyidagiga o‘xshash yozuv chiqadi:

```text
(.venv)
```

Windows:

```bash
python -m venv .venv
```

Aktivlashtirish:

```bash
.venv\Scripts\activate
```

---

# 📦 4. Python paketlarini o‘rnatish

`requirements.txt` mavjud bo‘lsa:

```bash
pip install -r requirements.txt
```

Yoki kerakli paketlarni alohida o‘rnatish:

```bash
pip install fastapi
pip install uvicorn
pip install chromadb
pip install ollama
pip install pymupdf
pip install python-dotenv
pip install pydantic
pip install pytest
```

---

# 🤖 5. Ollama o‘rnatish

Ollama lokal kompyuterda LLM va embedding modellarini ishga tushirish uchun ishlatiladi.

Ollama o‘rnatilgandan keyin tekshiring:

```bash
ollama --version
```

Agar versiya chiqsa, Ollama to‘g‘ri o‘rnatilgan.

Ollama serverini ishga tushirish:

```bash
ollama serve
```

Agar Ollama service avtomatik ishlayotgan bo‘lsa, bu buyruqni alohida ishga tushirish shart bo‘lmasligi mumkin.

---

# 🧠 6. Ollama modellari

Ushbu loyihada **ikki xil model** ishlatiladi.

## 6.1. Embedding modeli

Embedding uchun:

```text
nomic-embed-text:latest
```

O‘rnatish:

```bash
ollama pull nomic-embed-text:latest
```

Tekshirish:

```bash
ollama list
```

Natijada quyidagiga o‘xshash model ko‘rinishi kerak:

```text
NAME                        SIZE
nomic-embed-text:latest     ...
```

Bu model matnlarni vektorga aylantirish uchun ishlatiladi.

Masalan:

```text
"234-son qaror nima haqida?"
```

↓

```text
[0.012, -0.421, 0.183, ...]
```

Keyinchalik ushbu vector ChromaDB'dagi vectorlar bilan solishtiriladi.

---

# 🧠 6.2. LLM modeli

Savolga yakuniy javob berish uchun:

```text
qwen2.5:0.5b
```

modelidan foydalanish tavsiya qilinadi.

O‘rnatish:

```bash
ollama pull qwen2.5:0.5b
```

Tekshirish:

```bash
ollama list
```

Natijada:

```text
qwen2.5:0.5b
nomic-embed-text:latest
```

modellari mavjud bo‘lishi kerak.

Modelni test qilish:

```bash
ollama run qwen2.5:0.5b
```

Keyin:

```text
Salom
```

deb yozib ko‘ring.

Agar model javob bersa, Ollama va Qwen to‘g‘ri ishlayapti.

Chiqish:

```text
/bye
```

---

# 💡 Nima uchun ikkita model kerak?

RAG tizimida embedding modeli va LLM modeli turli vazifalarni bajaradi.

### `nomic-embed-text`

Vazifasi:

```text
Matn → Vector
```

Ya'ni:

```text
Savol
 ↓
Embedding
 ↓
Vector
```

### `qwen2.5:0.5b`

Vazifasi:

```text
Context + Question → Answer
```

Ya'ni:

```text
Savol
  +
234-son qarordan topilgan ma'lumot
  ↓
Qwen
  ↓
Javob
```

Shuning uchun **Qwen'ni embedding modeli sifatida ishlatmaymiz**.

---

# ⚠️ Muhim: Modellarni almashtirmang

Agar `.env` faylda:

```env
EMBEDDING_MODEL=nomic-embed-text:latest
```

bo‘lsa, Ollama'da aynan shu model bo‘lishi kerak:

```bash
ollama pull nomic-embed-text:latest
```

Agar:

```env
OLLAMA_MODEL=qwen2.5:0.5b
```

bo‘lsa:

```bash
ollama pull qwen2.5:0.5b
```

kerak.

Model nomlari bir xil bo‘lishi juda muhim.

---

# 🔐 7. `.env` fayl

Loyiha root papkasida:

```text
.env
```

fayl yarating.

Masalan:

```env
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=qwen2.5:0.5b

EMBEDDING_MODEL=nomic-embed-text:latest

CHROMA_PERSIST_DIRECTORY=./data/chroma

RETRIEVAL_TOP_K=5

RETRIEVAL_SCORE_THRESHOLD=0.5
```

---

# 📝 8. `.env.example`

GitHub repository'ga `.env` faylni yuklamaslik kerak.

Buning o‘rniga:

```text
.env.example
```

yarating.

Ichiga:

```env
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=qwen2.5:0.5b

EMBEDDING_MODEL=nomic-embed-text:latest

CHROMA_PERSIST_DIRECTORY=./data/chroma

RETRIEVAL_TOP_K=5

RETRIEVAL_SCORE_THRESHOLD=0.5
```

yozing.

`.env` esa `.gitignore` ichida bo‘lishi kerak:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
data/chroma/
```

---

# 📄 9. 234-son qaror

Asosiy hujjat:

```text
data/documents/qaror_234/source.pdf
```

Bu fayl 234-son qarorning original PDF hujjati hisoblanadi.

Pipeline:

```text
source.pdf
    ↓
extract_text.py
    ↓
qaror_234.txt
    ↓
chunk_document.py
    ↓
chunks.json
    ↓
ingest.py
    ↓
Embeddings
    ↓
ChromaDB
```

---

# 📑 10. PDF'dan text olish

PDF:

```text
data/documents/qaror_234/source.pdf
```

bo‘lishi kerak.

Text extraction script:

```bash
python scripts/extract_text.py
```

Natijada:

```text
data/documents/qaror_234/qaror_234.txt
```

yaratiladi.

---

# ✂️ 11. Document chunking

Katta hujjatni bir vaqtning o‘zida embedding qilish yaxshi usul emas.

Shuning uchun hujjat kichik qismlarga — **chunk**larga bo‘linadi.

Masalan:

```text
234-son qaror
      ↓
1500 belgilik chunklar
      ↓
Chunk 1
Chunk 2
Chunk 3
...
```

Overlap ham ishlatiladi.

Masalan:

```text
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
```

Bu bir chunk oxiridagi ma'lumotning keyingi chunk boshida ham qisman takrorlanishini ta'minlaydi.

Chunk yaratish:

```bash
python scripts/chunk_document.py
```

Natija:

```text
data/documents/qaror_234/chunks.json
```

---

# 🧮 12. Embedding va ChromaDB'ga yuklash

`chunks.json` tayyor bo‘lgandan keyin chunklar embedding qilinadi.

Embedding modeli:

```text
nomic-embed-text:latest
```

Ishga tushirish:

```bash
python scripts/ingest.py
```

Pipeline:

```text
chunks.json
     ↓
nomic-embed-text
     ↓
Vector
     ↓
ChromaDB
```

ChromaDB ma'lumotlari:

```text
data/chroma/
```

papkasida saqlanadi.

---

# 🔎 13. Retrieval

Foydalanuvchi savol beradi:

```text
Ekologik ekspertiza qachon o'tkaziladi?
```

Savol embedding qilinadi:

```text
Question
   ↓
nomic-embed-text
   ↓
Question Vector
```

Keyin ChromaDB'dan eng o‘xshash chunklar qidiriladi:

```text
Question Vector
      ↓
   ChromaDB
      ↓
Top 5 relevant chunks
```

`.env`:

```env
RETRIEVAL_TOP_K=5
```

bo‘lsa, eng mos 5 ta chunk olinadi.

---

# 🎯 14. Score threshold

Retrieval natijalarining relevance score'ini ham tekshirish mumkin.

```env
RETRIEVAL_SCORE_THRESHOLD=0.5
```

Bu mexanizm foydasiz yoki savolga aloqasi juda kam bo‘lgan chunklarni context'ga yubormaslikka yordam beradi.

Threshold qiymati embedding similarity/distance qanday hisoblanishiga bog‘liq bo‘lishi sababli, uni real testlar asosida sozlash kerak.

---

# 🤖 15. RAG orqali javob olish

Foydalanuvchi:

```text
Savol
```

yuboradi.

Backend:

```text
Question
   ↓
Embedding
   ↓
ChromaDB
   ↓
Relevant chunks
   ↓
Context
   ↓
Qwen 2.5 7B
   ↓
Answer
```

Qwen'ga faqat kerakli context beriladi.

Masalan:

```text
SYSTEM:
Siz 234-son qaror asosida javob beruvchi yordamchisiz.

Faqat berilgan CONTEXT asosida javob bering.

Agar javob CONTEXT ichida mavjud bo'lmasa:

"Bu ma'lumot 234-son qaror matnida topilmadi."

deb javob bering.

Foydalanuvchi savoliga uydirma ma'lumot qo'shmang.
```

---

# 🛡️ 16. Hallucination'ni kamaytirish

Loyihaning muhim talablaridan biri — modelning o‘z bilimidan foydalanib ketmasligi.

Shuning uchun RAG prompt quyidagi prinsip asosida ishlashi kerak:

```text
ONLY USE PROVIDED CONTEXT
```

Ya'ni:

```text
234-son qarorda bor
        ↓
      Javob ber

234-son qarorda yo'q
        ↓
"Ma'lumot topilmadi"
```

Model o‘zining umumiy bilimidan foydalanib javob bermasligi kerak.

---

# 🚀 17. FastAPI serverni ishga tushirish

Virtual environment aktiv bo‘lishi kerak:

```bash
source .venv/bin/activate
```

Keyin:

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

manzilda ishga tushadi.

---

# 📚 18. Swagger documentation

FastAPI avtomatik Swagger documentation yaratadi.

Brauzerda:

```text
http://127.0.0.1:8000/docs
```

oching.

Alternative:

```text
http://127.0.0.1:8000/redoc
```

---

# 💬 19. API'dan foydalanish

Masalan endpoint:

```text
POST /chat/
```

bo‘lsa, request:

```json
{
    "question": "234-son qaror nima haqida?"
}
```

Response:

```json
{
    "answer": "..."
}
```

Aniq request va response strukturasi FastAPI Swagger documentation'da ko‘rsatiladi.

---

# 🧪 20. Testlarni ishga tushirish

Test:

```bash
pytest
```

Verbose:

```bash
pytest -v
```

Faqat ma'lum test:

```bash
pytest tests/test_rag.py -v
```

---

# 🔧 21. Muammolarni tekshirish

## Ollama ishlayaptimi?

```bash
ollama list
```

Quyidagi modellar bo‘lishi kerak:

```text
qwen2.5:0.5b
nomic-embed-text:latest
```

---

## Qwen ishlayaptimi?

```bash
ollama run qwen2.5:0.5b
```

---

## Embedding modeli ishlayaptimi?

```bash
ollama run nomic-embed-text:latest "test matn"
```

Muhim:

```bash
ollama run nomic-embed-text:latest
```

deb bo‘sh ishga tushirilsa, embedding model input text talab qilishi mumkin.

Test uchun:

```bash
ollama run nomic-embed-text:latest "Bu test matni."
```

ishlatiladi.

---

# ❌ 22. `model not found` xatosi

Agar:

```text
model not found
```

xatosi chiqsa:

```bash
ollama list
```

orqali model nomini tekshiring.

Masalan `.env`:

```env
OLLAMA_MODEL=qwen2.5:0.5b
```

bo‘lsa:

```bash
ollama pull qwen2.5:0.5b
```

bajaring.

Embedding uchun:

```bash
ollama pull nomic-embed-text:latest
```

---

# ❌ 23. ChromaDB muammolari

Agar ChromaDB bilan muammo bo‘lsa:

```text
data/chroma/
```

papkasini tekshiring.

Agar embedding modeli o‘zgartirilgan bo‘lsa, eski embeddinglar bilan yangi embeddinglar mos kelmasligi mumkin.

Bunday holatda ChromaDB'ni qayta yaratib, ingestion'ni qayta bajarish kerak bo‘lishi mumkin:

```text
data/chroma/
```

→ eski vector database

keyin:

```bash
python scripts/ingest.py
```

---

# 🔄 24. To‘liq o‘rnatish tartibi

Yangi kompyuterda loyihani ishga tushirish:

### 1. Repository

```bash
git clone https://github.com/ilhomjondevuz/VM_234_RAG_API_fastAPI_app.git
cd VM_234_RAG_API_fastAPI_app
```

### 2. Virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Packages

```bash
pip install -r requirements.txt
```

### 4. Ollama

Ollama o‘rnatilganini tekshiring:

```bash
ollama --version
```

### 5. LLM

```bash
ollama pull qwen2.5:0.5b
```

### 6. Embedding

```bash
ollama pull nomic-embed-text:latest
```

### 7. Modellarni tekshirish

```bash
ollama list
```

Natijada:

```text
qwen2.5:0.5b
nomic-embed-text:latest
```

bo‘lishi kerak.

### 8. `.env`

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:0.5b
EMBEDDING_MODEL=nomic-embed-text:latest
CHROMA_PERSIST_DIRECTORY=./data/chroma
RETRIEVAL_TOP_K=5
RETRIEVAL_SCORE_THRESHOLD=0.5
```

### 9. PDF → text

```bash
python scripts/extract_text.py
```

### 10. Text → chunks

```bash
python scripts/chunk_document.py
```

### 11. Chunks → embeddings → ChromaDB

```bash
python scripts/ingest.py
```

### 12. API

```bash
uvicorn app.main:app --reload
```

### 13. Swagger

```text
http://127.0.0.1:8000/docs
```

---

# 📊 25. RAG pipeline'ning to‘liq ko‘rinishi

## Indexing vaqtida

```text
                 source.pdf
                     │
                     ▼
              PyMuPDF / fitz
                     │
                     ▼
               qaror_234.txt
                     │
                     ▼
                 Chunking
                     │
                     ▼
                chunks.json
                     │
                     ▼
            nomic-embed-text
                     │
                     ▼
                 Embeddings
                     │
                     ▼
                 ChromaDB
```

## User request vaqtida

```text
                 User Question
                       │
                       ▼
              nomic-embed-text
                       │
                       ▼
                 Query Vector
                       │
                       ▼
                    ChromaDB
                       │
                       ▼
             Relevant Chunks
                       │
                       ▼
                  RAG Context
                       │
                       ▼
                 Qwen 2.5 7B
                       │
                       ▼
                  Final Answer
```

---

# 🧠 26. Ollama modellari bo‘yicha qisqa jadval

| Model                     | Vazifasi            | Loyihadagi holati |
| ------------------------- | ------------------- | ----------------- |
| `nomic-embed-text:latest` | Embedding yaratish  | Majburiy          |
| `qwen2.5:0.5b`              | Javob generatsiyasi | Tavsiya etiladi   |

Embedding:

```text
nomic-embed-text
```

LLM:

```text
qwen2.5:0.5b
```

---

# 💻 27. Hardware tavsiyasi

`qwen2.5:0.5b` lokal ishlatilgani sababli RAM va CPU/GPU resurslari muhim.

Minimal ishlash muhiti qurilma konfiguratsiyasiga bog‘liq bo‘ladi, lekin modelni lokal ishlatishda yetarli RAM va imkon bo‘lsa GPU bo‘lishi javob tezligini sezilarli yaxshilaydi.

Agar kompyuter resurslari cheklangan bo‘lsa, Qwen'ning kichikroq variantidan foydalanish mumkin.

Masalan:

```bash
ollama pull qwen2.5:3b
```

va `.env`:

```env
OLLAMA_MODEL=qwen2.5:3b
```

Lekin ushbu loyiha uchun boshlang‘ich tavsiya:

```env
OLLAMA_MODEL=qwen2.5:0.5b
```

---

# 🔒 28. Git xavfsizligi

`.env` faylni GitHub'ga yuklamang.

`.gitignore`:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
*.pyc
data/chroma/
```

`source.pdf` kabi katta fayllarni repository'ga joylash masalasida repository hajmini ham hisobga olish kerak.

---

# 📌 29. Muhim buyruqlar

Ollama:

```bash
ollama list
```

Qwen:

```bash
ollama run qwen2.5:0.5b
```

Embedding:

```bash
ollama run nomic-embed-text:latest "test"
```

Model yuklash:

```bash
ollama pull qwen2.5:0.5b
ollama pull nomic-embed-text:latest
```

FastAPI:

```bash
uvicorn app.main:app --reload
```

Test:

```bash
pytest -v
```

PDF extraction:

```bash
python scripts/extract_text.py
```

Chunking:

```bash
python scripts/chunk_document.py
```

Ingestion:

```bash
python scripts/ingest.py
```

---

# 🎯 30. Loyihaning asosiy maqsadi

Ushbu loyiha:

1. 234-son qarorni PDF'dan o‘qiydi.
2. Matnni tozalaydi.
3. Matnni chunklarga bo‘ladi.
4. Chunklarni embedding qiladi.
5. Embeddinglarni ChromaDB'ga saqlaydi.
6. Foydalanuvchi savolini embedding qiladi.
7. ChromaDB'dan eng mos chunklarni topadi.
8. Topilgan ma'lumotlarni context sifatida Qwen'ga yuboradi.
9. Qwen faqat shu context asosida javob beradi.
10. Javob 234-son qaror mazmuniga asoslangan bo‘ladi.

---

# 🚀 Quick Start

Agar barcha dependency'lar o‘rnatilgan bo‘lsa:

```bash
source .venv/bin/activate

ollama pull qwen2.5:0.5b
ollama pull nomic-embed-text:latest

python scripts/extract_text.py
python scripts/chunk_document.py
python scripts/ingest.py

uvicorn app.main:app --reload
```

Keyin:

```text
http://127.0.0.1:8000/docs
```

manzilini oching.

---

# 👨‍💻 Development

Development server:

```bash
uvicorn app.main:app --reload
```

Production uchun `--reload` ishlatilmaydi.

Masalan:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# 📜 License

Ushbu loyiha ta'limiy va amaliy maqsadlarda ishlab chiqilgan.
