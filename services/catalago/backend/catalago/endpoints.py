from .contratos import resposta_v1, resposta_v2


def _consultar_recurso(servico, identificador, montar_resposta):
    registro = servico.consultar(identificador)

    if registro is None:
        return 404, {
            "erro": {
                "codigo": "RECURSO_INEXISTENTE",
                "id": identificador,
            }
        }

    return 200, montar_resposta(registro)


def consultar_recurso(servico, identificador):
    """Consulta com o contrato original da v1."""
    return _consultar_recurso(servico, identificador, resposta_v1)


def consultar_recurso_v2(servico, identificador):
    """Consulta com o contrato ampliado da v2."""
    return _consultar_recurso(servico, identificador, resposta_v2)
