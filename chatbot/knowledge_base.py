"""Pencarian jawaban lokal menggunakan TF-IDF dan cosine similarity.

Pertanyaan di luar cakupan FAQ harus menghasilkan None agar diteruskan ke Gemini.
Implementasi memakai standard library Python tanpa dependensi tambahan.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
SIMILARITY_THRESHOLD = 0.5

# Kata tanya/penghubung yang terlalu umum dan dapat menyebabkan kecocokan palsu.
STOPWORDS = {
    "apa", "apakah", "itu", "ini", "yang", "dan", "atau", "di", "ke",
    "dari", "untuk", "dengan", "bagaimana", "gimana", "cara", "siapa",
    "kapan", "dimana", "di mana", "mengapa", "kenapa", "jelaskan",
    "tolong", "saya", "aku", "ingin", "mau", "tentang", "adalah",
    "kah", "ya", "dong", "nya", "sebuah", "suatu", "berapa"
}


def _tokenize(text: str) -> list[str]:
    """Normalisasi teks dan buang kata umum agar pencocokan fokus pada topik."""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def _load_entries() -> list[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        entries = json.load(file)
    if not isinstance(entries, list):
        raise ValueError("Knowledge base harus berupa daftar JSON.")
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("answer"), str):
            raise ValueError("Setiap entri harus memiliki field answer berupa teks.")
        if not isinstance(entry.get("questions"), list):
            raise ValueError("Setiap entri harus memiliki field questions berupa daftar.")
    return entries


def _fit_idf(documents: list[list[str]]) -> dict[str, float]:
    total = len(documents)
    document_frequency: Counter[str] = Counter()
    for tokens in documents:
        document_frequency.update(set(tokens))
    return {
        token: math.log((1 + total) / (1 + frequency)) + 1
        for token, frequency in document_frequency.items()
    }


def _vectorize(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    counts = Counter(tokens)
    unknown = max(idf.values(), default=1.0)
    return {token: count * idf.get(token, unknown) for token, count in counts.items()}


def _cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(weight * right.get(token, 0.0) for token, weight in left.items())
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def find_answer(question: str) -> str | None:
    """Cari FAQ yang relevan; None berarti pertanyaan harus diteruskan ke Gemini."""
    if not isinstance(question, str) or not question.strip():
        return None

    entries = _load_entries()
    documents: list[list[str]] = []
    owners: list[int] = []
    for index, entry in enumerate(entries):
        for sample_question in entry["questions"]:
            if isinstance(sample_question, str) and sample_question.strip():
                documents.append(_tokenize(sample_question))
                owners.append(index)

    query_tokens = _tokenize(question)
    if not query_tokens or not documents:
        return None

    idf = _fit_idf(documents)
    vocabulary = set(idf)
    # Syarat penting: minimal satu kata topik dari pertanyaan harus ada di FAQ.
    # Tanpa ini, kata umum seperti "apa" atau "cara" bisa memicu jawaban yang salah.
    if not (set(query_tokens) & vocabulary):
        return None

    query_vector = _vectorize(query_tokens, idf)
    best_score = 0.0
    best_entry = None

    for tokens, owner in zip(documents, owners):
        score = _cosine_similarity(query_vector, _vectorize(tokens, idf))
        if score > best_score:
            best_score = score
            best_entry = entries[owner]

    if best_entry is None or best_score < SIMILARITY_THRESHOLD:
        return None
    return best_entry["answer"]
