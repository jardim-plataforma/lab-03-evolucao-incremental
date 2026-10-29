import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
from backend.catalogo.servico import ServicoCatalogo
from backend.catalogo.endpoints import consultar_recurso, consultar_recurso_v2

ROOT = Path(__file__).resolve().parents[1]
SERVICO = ServicoCatalogo()
ASSETS = {"/": ("index.html", "text/html; charset=utf-8"),
          "/app.js": ("app.js", "text/javascript; charset=utf-8"),
          "/style.css": ("style.css", "text/css; charset=utf-8")}

class Handler(BaseHTTPRequestHandler):
    def responder(self, status, body, content_type="application/json; charset=utf-8"):
        data = json.dumps(body, ensure_ascii=False).encode() if isinstance(body, dict) else body
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == "/health":
            return self.responder(200, {"status": "ok", "version": (ROOT/"VERSION").read_text().strip()})
        if path in ASSETS:
            name, mime = ASSETS[path]
            return self.responder(200, (ROOT/"frontend"/name).read_bytes(), mime)

        prefix_v2 = "/api/v2/recursos/"
        if path.startswith(prefix_v2) and path[len(prefix_v2):] and "/" not in path[len(prefix_v2):]:
            status, body = consultar_recurso_v2(SERVICO, path[len(prefix_v2):])
            return self.responder(status, body)

        prefix_v1 = "/api/v1/recursos/"
        if path.startswith(prefix_v1) and path[len(prefix_v1):] and "/" not in path[len(prefix_v1):]:
            status, body = consultar_recurso(SERVICO, path[len(prefix_v1):])
            return self.responder(status, body)

        self.responder(404, {"erro": {"codigo": "ROTA_INEXISTENTE"}})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Catálogo local: http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
