import unittest
from backend.catalogo.servico import ServicoCatalogo
from backend.catalogo.endpoints import consultar_recurso


class AusenciaTest(unittest.TestCase):
    def test_recurso_inexistente(self):
        status, payload = consultar_recurso(ServicoCatalogo(), "ausente")
        self.assertEqual(status, 404)
        self.assertEqual(payload, {"erro": {"codigo": "RECURSO_INEXISTENTE", "id": "ausente"}})
