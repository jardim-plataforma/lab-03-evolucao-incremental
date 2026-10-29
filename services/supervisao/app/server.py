import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .estado import carregar


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            code, body = 200, {'status': 'ok', 'servico': 'supervisao'}
        elif self.path == '/estado':
            code, body = 200, carregar()
        else:
            code, body = 404, {'erro': 'ROTA_INEXISTENTE'}
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8090)
    args = parser.parse_args()
    carregar()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Supervisão local: http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
