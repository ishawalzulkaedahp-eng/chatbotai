import io
import json
import os
import unittest
from unittest.mock import patch

from chatbot import llm

ENV = {"API_AI_KEY": "kunci-palsu", "API_AI_MODEL": "model-palsu"}


def respons_palsu(teks):
    data = {"candidates": [{"content": {"parts": [{"text": teks}]}}]}
    resp = io.BytesIO(json.dumps(data).encode("utf-8"))
    resp.__enter__ = lambda s=resp: s
    resp.__exit__ = lambda *a: False
    return resp


class TestLLM(unittest.TestCase):
    def test_jawaban_berhasil(self):
        with patch.dict(os.environ, ENV), \
             patch("chatbot.llm.urllib.request.urlopen", return_value=respons_palsu(" Halo! ")) as kirim:
            self.assertEqual(llm.ask_llm("hai"), "Halo!")
        permintaan = kirim.call_args[0][0]
        self.assertIn("model-palsu", permintaan.full_url)
        self.assertEqual(permintaan.get_header("X-goog-api-key"), "kunci-palsu")

    def test_key_kosong(self):
        with patch.dict(os.environ, {**ENV, "API_AI_KEY": ""}):
            with self.assertRaises(ValueError):
                llm.ask_llm("hai")

    def test_api_gagal(self):
        with patch.dict(os.environ, ENV), \
             patch("chatbot.llm.urllib.request.urlopen", side_effect=Exception("rahasia")):
            with self.assertRaises(RuntimeError) as ctx:
                llm.ask_llm("hai")
        self.assertNotIn("rahasia", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()