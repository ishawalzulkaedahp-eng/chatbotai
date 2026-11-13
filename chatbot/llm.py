import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv()  # baca isi file .env

# Jalur asli Gemini. Key format baru (diawali "AQ.") belum didukung
# di jalur OpenAI-compatible, jadi kita pakai jalur ini.
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
TIMEOUT_DETIK = 60
# Kode error yang artinya "coba model lain": model penuh, kuota habis, atau model tidak tersedia.
COBA_MODEL_LAIN = {404, 429, 500, 503}


def _tanya_satu_model(model: str, api_key: str, question: str) -> str:
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
    with urllib.request.urlopen(request, timeout=TIMEOUT_DETIK) as response:
        data = json.load(response)
    parts = data["candidates"][0]["content"]["parts"]
    return "".join(part.get("text", "") for part in parts)


def ask_llm(question: str) -> str:
    api_key = os.getenv("API_AI_KEY")
    # Boleh lebih dari satu model, dipisah koma. Model pertama dicoba dulu.
    models = [m.strip() for m in (os.getenv("API_AI_MODEL") or "").split(",") if m.strip()]
    if not (api_key and models):
        raise ValueError("Konfigurasi LLM di .env belum lengkap.")

    for model in models:
        try:
            answer = _tanya_satu_model(model, api_key, question)
        except urllib.error.HTTPError as error:
            if error.code in COBA_MODEL_LAIN:
                continue  # model ini sedang penuh/tidak ada, coba model berikutnya
            break  # error lain (misalnya key salah): tidak ada gunanya mencoba lagi
        except Exception:
            continue  # timeout atau koneksi putus: coba model berikutnya
        if answer.strip():
            return answer.strip()

    # Jangan tampilkan detail error asli: bisa berisi info rahasia
    raise RuntimeError("Layanan AI sedang tidak tersedia.")