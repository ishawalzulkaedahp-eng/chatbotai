import unittest

from chatbot.knowledge_base import find_answer


class TestKnowledgeBase(unittest.TestCase):
    def test_pertanyaan_dikenali(self):
        self.assertIn("Universitas Negeri Padang", find_answer("apa itu UNP"))

    def test_variasi_pertanyaan_dikenali(self):
        self.assertIn("Kartu Rencana Studi", find_answer("bagaimana cara mengisi KRS"))

    def test_pertanyaan_tidak_relevan_mengembalikan_none(self):
        self.assertIsNone(find_answer("resep membuat rendang"))

    def test_input_kosong_mengembalikan_none(self):
        self.assertIsNone(find_answer("   "))


if __name__ == "__main__":
    unittest.main()
