import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen
from app.server import Handler


class HttpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_saude_e_estado(self):
        for route, expected in [('/health', 'ok'), ('/estado', 'operacional')]:
            with self.subTest(route=route):
                with urlopen(self.base + route, timeout=3) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(json.load(response)['status'], expected)

    def test_rota_ausente(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base + '/ausente', timeout=3)
        self.assertEqual(error.exception.code, 404)
