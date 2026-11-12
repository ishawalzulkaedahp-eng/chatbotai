# Chatbot AI

Chatbot mencari jawaban di knowledge base dulu. Kalau tidak ada, bertanya ke Gemini.

## Pembagian tugas
| Orang | Bagian | File |
|---|---|---|
| 1 | Struktur + backend | main.py, backend/server.py, chatbot/service.py |
| 2 | Web | web/index.html, web/style.css, web/app.js |
| 3 | Knowledge base | data/knowledge_base.json, chatbot/knowledge_base.py |
| 4 | LLM (Gemini) | chatbot/llm.py |

## Kontrak fungsi
- `find_answer(question)` mengembalikan teks jawaban, atau `None` kalau tidak ketemu
- `ask_llm(question)` mengembalikan teks jawaban dari Gemini
- `answer(question)` mengembalikan `{"answer": "...", "source": "knowledge_base" / "llm"}`
- Web mengirim `POST /api/chat` dengan body `{"question": "..."}`

## Cara menjalankan
```
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env   # lalu isi API key Gemini sendiri
.\.venv\Scripts\python main.py
```
Buka http://127.0.0.1:8000/