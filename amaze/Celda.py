from Direcccion import Direccion
class Celda():
    def __init__(self):
        self.visited = False
        self.walls = {
            Direccion.NORTE: True,
            Direccion.SUR: True,
            Direccion.ESTE: True,
            Direccion.OESTE: True
        }
        self.es_42 = False