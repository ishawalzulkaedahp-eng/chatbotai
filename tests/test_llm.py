
import os
import unittest
from unittest.mock import MagicMock, patch

from chatbot import llm


ENV = {
    "API_AI_KEY": "kunci-palsu",
    "API_AI_BASE_URL": "https://contoh",
    "API_AI_MODEL": "model"
}


class TestLLM(unittest.TestCase):

    def test_jawaban_berhasil(self):
        palsu = MagicMock()
        palsu.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content=" Halo! "))
        ]

        with patch.dict(os.environ, ENV), \
             patch("chatbot.llm.OpenAI", return_value=palsu):

            hasil = llm.ask_llm("hai")
            self.assertEqual(hasil, "Halo!")

    def test_key_kosong(self):
        env_kosong = {**ENV, "API_AI_KEY": ""}

        with patch.dict(os.environ, env_kosong):
            with self.assertRaises(ValueError):
                llm.ask_llm("hai")

    def test_api_gagal(self):
        palsu = MagicMock()
        palsu.chat.completions.create.side_effect = Exception("rahasia")

        with patch.dict(os.environ, ENV), \
             patch("chatbot.llm.OpenAI", return_value=palsu):

            with self.assertRaises(RuntimeError) as ctx:
                llm.ask_llm("hai")

            self.assertNotIn("rahasia", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
