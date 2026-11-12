import unittest
from unittest.mock import patch

from chatbot.service import answer


class TestService(unittest.TestCase):
    # Tes 1: kalau jawaban ada di knowledge base, AI TIDAK boleh dipanggil
    def test_jawaban_lokal_tidak_panggil_ai(self):
        with patch("chatbot.service.find_answer", return_value="Jawaban lokal"), \
             patch("chatbot.service.ask_llm") as llm:
            hasil = answer("halo")
        self.assertEqual(hasil, {"answer": "Jawaban lokal", "source": "knowledge_base"})
        llm.assert_not_called()

    # Tes 2: kalau tidak ketemu di knowledge base, pakai jawaban AI
    def test_pakai_ai_kalau_tidak_ketemu(self):
        with patch("chatbot.service.find_answer", return_value=None), \
             patch("chatbot.service.ask_llm", return_value="Jawaban AI"):
            hasil = answer("halo")
        self.assertEqual(hasil, {"answer": "Jawaban AI", "source": "llm"})

    # Tes 3: pertanyaan kosong harus ditolak
    def test_input_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            answer("   ")


if __name__ == "__main__":
    unittest.main()