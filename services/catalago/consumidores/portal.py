"""Consumidor A: usa os campos de que precisa, tolerando campos adicionais."""
def interpretar(payload):
    for campo in ("id", "nome", "status"):
        if not isinstance(payload.get(campo), str) or not payload[campo]:
            raise ValueError(f"Campo obrigatório inválido: {campo}")
    return f"{payload['nome']} — {payload['status']}"
