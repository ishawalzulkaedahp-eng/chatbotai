import unittest

from chatbot.knowledge_base import find_answer


class TestKnowledgeBase(unittest.TestCase):
    def test_pertanyaan_dikenali(self):
        self.assertIn("Universitas Negeri Padang", find_answer("apa itu UNP"))

    def test_variasi_pertanyaan_dikenali(self):
        self.assertIn("Kartu Rencana Studi", find_answer("bagaimana cara mengisi KRS"))

    def test_pertanyaan_tidak_relevan_mengembalikan_none(self):
        self.assertIsNone(find_answer("resep membuat rendang"))

    def test_topik_umum_di_luar_faq_diteruskan_ke_gemini(self):
        self.assertIsNone(find_answer("apa itu python?"))
        self.assertIsNone(find_answer("siapa presiden indonesia"))
        self.assertIsNone(find_answer("bagaimana cara membuat website"))

    def test_pertanyaan_akademik_lain_tetap_dikenali(self):
        self.assertIsNotNone(find_answer("cuti kuliah gimana"))
        self.assertIsNotNone(find_answer("cara isi KRS"))

    def test_input_kosong_mengembalikan_none(self):
        self.assertIsNone(find_answer("   "))


if __name__ == "__main__":
    unittest.main()
