
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def ask_llm(question: str) -> str:
    api_key = os.getenv("API_AI_KEY")
    base_url = os.getenv("API_AI_BASE_URL")
    model = os.getenv("API_AI_MODEL")

    if not (api_key and base_url and model):
        raise ValueError("Konfigurasi LLM di .env belum lengkap.")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=30
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Jawab singkat dan jelas dalam bahasa Indonesia."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
        )

        answer = response.choices[0].message.content

    except Exception:
        raise RuntimeError("Layanan AI sedang tidak tersedia.") from None

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("AI tidak memberikan jawaban.")

    return answer.strip()
