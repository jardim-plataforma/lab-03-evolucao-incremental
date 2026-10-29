"""Sonda de aceite. Ainda não existe uma interface pronta para atendê-la."""
import argparse
import json
from urllib.request import urlopen

def interpretar(payload):
    campos = {"id", "nome", "status", "unidade", "responsavel"}
    if not campos.issubset(payload):
        raise ValueError("Novo consumidor precisa dos cinco campos")
    if any(not isinstance(payload[campo], str) or not payload[campo] for campo in campos):
        raise ValueError("Os cinco campos devem conter texto não vazio")
    return {campo: payload[campo] for campo in sorted(campos)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL da interface escolhida na sua solução")
    args = parser.parse_args()
    with urlopen(args.url, timeout=5) as response:
        print(interpretar(json.load(response)))
