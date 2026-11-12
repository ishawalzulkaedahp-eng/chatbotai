from chatbot.knowledge_base import find_answer
from chatbot.llm import ask_llm


def answer(question: str) -> dict[str, str]:
    # 1. Tolak pertanyaan yang kosong atau terlalu panjang
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise ValueError("Pertanyaan harus 1 sampai 2000 karakter.")

    question = question.strip()

    # 2. Cari di knowledge base dulu (gratis dan cepat)
    jawaban_lokal = find_answer(question)
    if jawaban_lokal is not None:
        return {"answer": jawaban_lokal, "source": "knowledge_base"}

    # 3. Kalau tidak ada, baru tanya AI
    jawaban_ai = ask_llm(question)
    if not isinstance(jawaban_ai, str) or not jawaban_ai.strip():
        raise RuntimeError("AI mengembalikan jawaban kosong.")
    return {"answer": jawaban_ai.strip(), "source": "llm"}