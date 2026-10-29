"""Leitura de um relatório local de supervisão; não executa sondagens externas."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / 'config' / 'checks.json'


def resumir(checks):
    if not isinstance(checks, list) or not checks:
        raise ValueError('O relatório precisa conter pelo menos uma verificação')
    nomes = set()
    for check in checks:
        if (not isinstance(check, dict) or not isinstance(check.get('nome'), str)
            or not check['nome'].strip() or type(check.get('disponivel')) is not bool):
            raise ValueError('Verificação inválida')
        if check['nome'] in nomes:
            raise ValueError('Nome de verificação duplicado')
        nomes.add(check['nome'])
    indisponiveis = [item['nome'] for item in checks if not item['disponivel']]
    return {'status': 'degradado' if indisponiveis else 'operacional',
            'total': len(checks), 'indisponiveis': indisponiveis}


def carregar():
    return resumir(json.loads(REPORT.read_text(encoding='utf-8')))
