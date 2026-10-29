import unittest
from backend.catalogo.servico import ServicoCatalogo
from backend.catalogo.endpoints import consultar_recurso
from consumidores.portal import interpretar as portal
from consumidores.integracao import interpretar as integracao
from consumidores.novo_consumidor import interpretar as novo

class ContratosTest(unittest.TestCase):
    def setUp(self):
        self.status, self.payload = consultar_recurso(ServicoCatalogo(), "svc-001")

    def test_consulta_existente(self):
        self.assertEqual(self.status, 200)
        self.assertEqual(self.payload, {"id":"svc-001", "nome":"Consulta de unidades", "status":"ativo"})

    def test_portal_atual(self):
        self.assertIn("Consulta de unidades", portal(self.payload))

    def test_integracao_atual(self):
        self.assertEqual(integracao(self.payload)[0], "svc-001")

    def test_perfis_diferentes_de_tolerancia(self):
        ampliado = dict(self.payload, unidade="Operações", responsavel="Equipe Aurora")
        portal(ampliado)
        with self.assertRaises(ValueError):
            integracao(ampliado)
        novo(ampliado)

    def test_fonte_possui_dados_para_evolucao(self):
        registro = ServicoCatalogo().consultar("svc-001")
        self.assertEqual(registro["unidade"], "Operações")

    def test_fonte_nao_encontra_recurso(self):
        self.assertIsNone(ServicoCatalogo().consultar("inexistente"))
