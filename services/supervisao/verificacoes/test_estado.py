import unittest
from app.estado import carregar, resumir


class EstadoTest(unittest.TestCase):
    def test_relatorio_operacional(self):
        self.assertEqual(carregar(), {'status': 'operacional', 'total': 2,
                                      'indisponiveis': []})

    def test_degradacao(self):
        resultado = resumir([{'nome': 'fila', 'disponivel': False}])
        self.assertEqual(resultado['status'], 'degradado')
        self.assertEqual(resultado['indisponiveis'], ['fila'])

    def test_relatorio_vazio_nao_equivale_a_sucesso(self):
        with self.assertRaises(ValueError):
            resumir([])

    def test_booleano_obrigatorio(self):
        with self.assertRaises(ValueError):
            resumir([{'nome': 'fila', 'disponivel': 'false'}])

    def test_nomes_duplicados(self):
        with self.assertRaises(ValueError):
            resumir([{'nome': 'fila', 'disponivel': True},
                     {'nome': 'fila', 'disponivel': False}])
