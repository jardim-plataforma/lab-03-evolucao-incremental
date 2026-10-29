from .repositorio import RepositorioCatalogo

class ServicoCatalogo:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio or RepositorioCatalogo()

    def consultar(self, identificador):
        return self.repositorio.buscar(identificador)
