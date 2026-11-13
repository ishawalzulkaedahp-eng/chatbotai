# Chatbot AI – Asisten Akademik Sistem Informasi UNP

Chatbot berbasis web yang menjawab pertanyaan seputar akademik. Pertanyaan dicari dulu
di knowledge base (FAQ). Kalau tidak ditemukan, pertanyaan diteruskan ke Gemini AI.

## Anggota dan pembagian tugas
| Nama | Peran | File |
|---|---|---|
| Ishawal Zulkaedah Putri | Ketua: struktur proyek, backend, integrasi | `main.py`, `backend/server.py`, `chatbot/service.py`, `tests/test_service.py` |
| Hanifa Salsabila | Web (tampilan chat) | `web/index.html`, `web/style.css`, `web/app.js` |
| Salwa Rachelia | Knowledge base (19 FAQ) | `data/knowledge_base.json`, `chatbot/knowledge_base.py`, `tests/test_knowledge_base.py` |
| Rilvia Sherenina | Koneksi Gemini AI | `chatbot/llm.py`, `tests/test_llm.py` |

## Alur kerja chatbot
1. Pengguna mengetik pertanyaan di halaman web.
2. Web mengirim pertanyaan ke server (`POST /api/chat`).
3. Server mencari jawaban di knowledge base (pencocokan TF-IDF dan cosine similarity).
4. Jika tidak ditemukan, pertanyaan diteruskan ke Gemini AI.
5. Jawaban ditampilkan di web beserta sumbernya: **Knowledge Base** atau **Gemini AI**.

## Kontrak fungsi
- `find_answer(question)` mengembalikan teks jawaban, atau `None` kalau tidak ditemukan
- `ask_llm(question)` mengembalikan teks jawaban dari Gemini
- `answer(question)` mengembalikan `{"answer": "...", "source": "knowledge_base" / "llm"}`
- Web mengirim `POST /api/chat` dengan body `{"question": "..."}`

## Cara menjalankan
Butuh Python 3.10 atau lebih baru.

```
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env
```

Isi file `.env` dengan API key Gemini sendiri (buat di aistudio.google.com):

```
API_AI_KEY=key_gemini_kamu
API_AI_MODEL=gemini-3.6-flash,gemini-3.5-flash,gemini-3.8-flash
```

`API_AI_MODEL` boleh berisi beberapa model yang dipisah koma. Kalau satu model sedang penuh,
chatbot otomatis mencoba model berikutnya.

Jalankan server:

```
.\.venv\Scripts\python main.py
```

Lalu buka http://127.0.0.1:8000/ di browser.

## Menjalankan tes
```
.\.venv\Scripts\python -m unittest discover -s tests -v
```
Semua 14 tes harus lulus.

## Catatan
- File `.env` berisi API key dan tidak diunggah ke GitHub.
- Google kini menerbitkan API key Gemini dengan awalan `AQ.`. Key ini belum didukung jalur
  OpenAI-compatible, sehingga `chatbot/llm.py` memakai jalur asli Gemini (`generateContent`).
