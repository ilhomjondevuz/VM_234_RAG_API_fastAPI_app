# VM 234 RAG API

Vazirlar Mahkamasining 234-son qarori matni asosida foydalanuvchi savollariga aniq javob beruvchi **RAG (Retrieval-Augmented Generation)** API.

## Loyiha arxitekturasi

```text
Foydalanuvchi
     │
     ▼
  FastAPI
     │
     ▼
   Savol
     │
     ▼
  Embedding
     │
     ▼
  ChromaDB
     │
     │ 234-son qaroridan
     │ mos ma'lumotlarni topadi
     ▼
Relevant chunks
     │
     ▼
   Ollama
     │
     ▼
    Qwen
     │
     ▼
   Javob
```

## Texnologiyalar

* Python
* FastAPI
* Ollama
* Qwen
* ChromaDB
* RAG
* Embeddings

---

# 1. Repository'ni clone qilish

```bash
git clone https://github.com/ilhomjondevuz/VM_234_RAG_API_fastAPI_app.git
cd VM_234_RAG_API_fastAPI_app
```

---

# 2. Virtual environment yaratish

Linux / Ubuntu:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Virtual environment faollashgandan keyin terminal boshida:

```text
(.venv)
```

ko‘rinadi.

---

# 3. Dependencies o‘rnatish

```bash
pip install -r requirements.txt
```

---

# 4. Ollama o‘rnatish

Ollama — LLM modellarini lokal kompyuterda ishga tushirish uchun ishlatiladi.

U **Linux, Windows va macOS** tizimlarida ishlaydi.

## Ubuntu / Linux

Terminalni oching va:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

buyrug‘ini bajaring.

Bu Ollama'ning rasmiy Linux o‘rnatish usuli.

O‘rnatilganini tekshirish:

```bash
ollama -v
```

Agar versiya chiqsa, Ollama muvaffaqiyatli o‘rnatilgan.

Masalan:

```text
ollama version ...
```

### Ollama serverini ishga tushirish

```bash
ollama serve
```

Agar Ollama system service sifatida o‘rnatilgan bo‘lsa, uni quyidagicha boshqarish mumkin:

```bash
sudo systemctl start ollama
```

Holatini tekshirish:

```bash
sudo systemctl status ollama
```

Ollama API odatda quyidagi manzilda ishlaydi:

```text
http://localhost:11434
```

---

# 5. Windows

Ollama Windows'da native application sifatida ishlaydi.

Windows 10 22H2 yoki undan yangi versiyasi talab qilinadi.

### Variant 1 — PowerShell orqali

PowerShell'ni ochib:

```powershell
irm https://ollama.com/install.ps1 | iex
```

buyrug‘ini bajaring.

Bu Ollama'ning rasmiy o‘rnatish usullaridan biri.

### Variant 2 — Installer orqali

Ollama'ning rasmiy Windows installerini yuklab olib o‘rnatish mumkin:

```text
OllamaSetup.exe
```

Windows installer administrator huquqini talab qilmaydi va odatda foydalanuvchi accountiga o‘rnatiladi.

O‘rnatilgandan keyin PowerShell yoki CMD'ni qayta ochib:

```powershell
ollama -v
```

deb tekshiring.

---

# 6. Ollama ishlayotganini tekshirish

Ollama o‘rnatilgandan keyin:

```bash
ollama
```

buyrug‘ini ishlatish mumkin.

Yoki modelni to‘g‘ridan-to‘g‘ri ishga tushirish:

```bash
ollama run qwen3
```

Model birinchi marta ishlatilganda Ollama uni yuklab oladi.

> Eslatma: model hajmi katta bo‘lishi mumkin. Model tanlashda kompyuteringizdagi RAM, GPU va disk hajmini hisobga oling.

---

# 7. Qwen modelini o‘rnatish

Ushbu loyiha uchun Qwen modelidan foydalaniladi.

Masalan:

```bash
ollama run qwen3
```

Modelni yuklab olib, interaktiv chatni boshlaydi.

Sinab ko‘rish:

```text
>>> Salom
```

Qwen javob bersa, Ollama + Qwen muvaffaqiyatli ishlayapti.

O‘rnatilgan modellarni ko‘rish:

```bash
ollama list
```

Masalan:

```text
NAME       ID       SIZE
qwen3      ...      ...
```

---

# 8. Ollama API

Ollama lokal API server sifatida ham ishlaydi.

Standart API manzili:

```text
http://localhost:11434
```

Tekshirish:

```bash
curl http://localhost:11434/api/tags
```

Agar Ollama ishlayotgan bo‘lsa, o‘rnatilgan modellar haqida JSON ma'lumot qaytadi.

Ollama REST API orqali Python/FastAPI loyihasidan ham foydalanish mumkin.

---

# 9. RAG qanday ishlaydi?

Ushbu loyihada 234-son qarorining PDF fayli avval matnga aylantiriladi.

```text
source.pdf
    │
    ▼
Text
    │
    ▼
Chunks
    │
    ▼
Embeddings
    │
    ▼
ChromaDB
```

Foydalanuvchi savol berganda:

```text
Savol
  │
  ▼
Embedding
  │
  ▼
ChromaDB
  │
  ▼
Relevant chunks
  │
  ▼
Qwen
  │
  ▼
Javob
```

Shu sababli Qwen faqat umumiy bilimiga tayanib javob bermaydi, balki **234-son qaroridan topilgan relevant ma'lumotlar asosida javob yaratadi**.

---

# 10. FastAPI'ni ishga tushirish

Virtual environment faolligini tekshiring:

```bash
source .venv/bin/activate
```

Linux uchun.

Windows:

```powershell
.venv\Scripts\activate
```

Keyin FastAPI serverini ishga tushiring:

```bash
uvicorn app.main:app --reload
```

Agar `main.py` boshqa joyda bo‘lsa, `uvicorn` yo‘lini loyihadagi structure'ga moslang.

API odatda:

```text
http://127.0.0.1:8000
```

manzilida ishlaydi.

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 11. Ishlash tartibi

To‘liq tizim quyidagicha ishlaydi:

```text
                    234-son qaror
                          │
                          ▼
                       PDF/TXT
                          │
                          ▼
                       Chunks
                          │
                          ▼
                      Embedding
                          │
                          ▼
                       ChromaDB
                          ▲
                          │
                          │
Foydalanuvchi ───────► FastAPI
   savoli                │
                          ▼
                      Embedding
                          │
                          ▼
                   Relevant chunks
                          │
                          ▼
                   Ollama + Qwen
                          │
                          ▼
                       Javob
```

---

# 12. Muhim buyruqlar

### Ollama versiyasini tekshirish

```bash
ollama -v
```

### Modellarni ko‘rish

```bash
ollama list
```

### Qwen'ni ishga tushirish

```bash
ollama run qwen3
```

### Ollama serverini ishga tushirish

```bash
ollama serve
```

### Ollama API'ni tekshirish

```bash
curl http://localhost:11434/api/tags
```

### FastAPI'ni ishga tushirish

```bash
uvicorn app.main:app --reload
```

---

# 13. Foydali rasmiy havolalar

* Ollama Documentation
* Ollama Linux Installation
* Ollama Windows Installation
* Ollama Quickstart

---

# 14. Eslatma

Ollama **model emas**.

```text
Ollama = modelni ishga tushiruvchi platforma
Qwen   = AI/LLM modeli
RAG    = kerakli hujjat ma'lumotini topib, LLM yordamida javob yaratish arxitekturasi
```

Ushbu loyihada:

```text
FastAPI → RAG → ChromaDB → Ollama → Qwen
```

zanjiri orqali foydalanuvchi savollariga 234-son qaror asosida javob beriladi.
