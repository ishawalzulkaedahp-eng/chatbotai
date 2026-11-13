import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv()  # baca isi file .env

# Jalur asli Gemini. Key format baru (diawali "AQ.") belum didukung
# di jalur OpenAI-compatible, jadi kita pakai jalur ini.
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def ask_llm(question: str) -> str:
    api_key = os.getenv("API_AI_KEY")
    model = os.getenv("API_AI_MODEL")
    if not (api_key and model):
        raise ValueError("Konfigurasi LLM di .env belum lengkap.")

    body = {
        "systemInstruction": {"parts": [{"text": "Jawab singkat dan jelas dalam bahasa Indonesia."}]},
        "contents": [{"role": "user", "parts": [{"text": question}]}],
    }
    request = urllib.request.Request(
        GEMINI_URL.format(model=model),
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        parts = data["candidates"][0]["content"]["parts"]
        answer = "".join(part.get("text", "") for part in parts)
    except Exception:
        # Jangan tampilkan detail error asli: bisa berisi info rahasia
        raise RuntimeError("Layanan AI sedang tidak tersedia.") from None

    if not answer.strip():
        raise RuntimeError("AI tidak memberikan jawaban.")
    return answer.strip()