import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from chatbot.service import answer

WEB_DIR = Path(__file__).resolve().parent.parent / "web"

STATIC_ROUTES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}


class ChatHandler(BaseHTTPRequestHandler):
    def send_body(self, status, body, content_type, headers=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_json(self, status, data, headers=None):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_body(status, body, "application/json; charset=utf-8", headers)

    def reject_method(self):
        path = urlsplit(self.path).path
        if path in STATIC_ROUTES or path == "/api/chat":
            allow = "POST" if path == "/api/chat" else "GET, HEAD"
            self.send_json(405, {"error": "Metode tidak diizinkan."}, {"Allow": allow})
        else:
            self.send_json(404, {"error": "Rute tidak ditemukan."})

    def do_GET(self):
        route = STATIC_ROUTES.get(urlsplit(self.path).path)
        if route is None:
            self.reject_method()
            return
        filename, content_type = route
        try:
            body = (WEB_DIR / filename).read_bytes()
        except OSError:
            self.send_json(500, {"error": "File web gagal dibaca."})
            return
        self.send_body(200, body, content_type)

    do_HEAD = do_GET
    do_PUT = do_PATCH = do_DELETE = reject_method

    def do_POST(self):
        if urlsplit(self.path).path != "/api/chat":
            self.reject_method()
            return
        if self.headers.get_content_type() != "application/json":
            self.send_json(415, {"error": "Content-Type harus application/json."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Content-Length tidak valid."})
            return
        if length > 16 * 1024:
            self.send_json(413, {"error": "Body request terlalu besar."})
            return
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, RecursionError):
            self.send_json(400, {"error": "Body JSON tidak valid."})
            return
        question = data.get("question") if isinstance(data, dict) else None
        if not isinstance(question, str) or not question.strip() or len(question) > 2000:
            self.send_json(400, {"error": "Pertanyaan harus 1 sampai 2.000 karakter."})
            return

        try:
            result = answer(question)
        except (ValueError, OSError):
            self.send_json(500, {"error": "Knowledge base atau konfigurasi tidak valid."})
        except RuntimeError:
            self.send_json(502, {"error": "Layanan AI gagal merespons. Coba lagi nanti."})
        else:
            self.send_json(200, result)


def run() -> None:
    with ThreadingHTTPServer(("127.0.0.1", 8000), ChatHandler) as server:
        print("Chatbot aktif di http://127.0.0.1:8000/ (Ctrl+C untuk berhenti)", flush=True)
        server.serve_forever()