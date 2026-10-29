import json
from pathlib import Path

class RepositorioCatalogo:
    def __init__(self, arquivo=None):
        arquivo = arquivo or Path(__file__).with_name("dados.json")
        self.registros = json.loads(Path(arquivo).read_text(encoding="utf-8"))

    def buscar(self, identificador):
        return next((dict(item) for item in self.registros if item["id"] == identificador), None)
