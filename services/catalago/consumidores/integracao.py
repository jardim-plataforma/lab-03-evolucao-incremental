"""Consumidor B: legado com validação estrita do contrato recebido."""
def interpretar(payload):
    if set(payload) != {"id", "nome", "status"}:
        raise ValueError("Contrato legado rejeitado: campos inesperados ou ausentes")
    if any(not isinstance(value, str) or not value for value in payload.values()):
        raise ValueError("Contrato legado rejeitado: tipo ou valor inválido")
    return (payload["id"], payload["nome"], payload["status"])
