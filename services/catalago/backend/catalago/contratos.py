def resposta_v1(registro):
    """Contrato público existente; mantém os três campos originais."""
    return {campo: registro[campo] for campo in ("id", "nome", "status")}


def resposta_v2(registro):
    """Contrato ampliado para o novo consumidor."""
    campos = ("id", "nome", "status", "unidade", "responsavel")
    return {campo: registro[campo] for campo in campos}
