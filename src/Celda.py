from .Direcccion import Direccion
class Celda():
    def __init__(self, a,b,c,d):
        self.walls = {
            Direccion.OESTE: a,
            Direccion.SUR: b,
            Direccion.ESTE: c,
            Direccion.NORTE: d
        }