from .Direcccion import Direccion
class Celda():
    def __init__(self, a,b,c,d, bool_42 = False):
        self.walls = {
            Direccion.OESTE: a,
            Direccion.SUR: b,
            Direccion.ESTE: c,
            Direccion.NORTE: d
        }
        casilla_42 = bool_42