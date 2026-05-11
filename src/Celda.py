from .Direcccion import Direccion


class Celda():
    def __init__(self,
                 a: int,
                 b: int,
                 c: int,
                 d: int,
                 bool_42: bool) -> None:
        self.walls = {
            Direccion.OESTE: a,
            Direccion.SUR: b,
            Direccion.ESTE: c,
            Direccion.NORTE: d
        }
        self.casilla_42 = bool_42

    def bin_to_hexa(self) -> str:
        oeste = int(self.walls[Direccion.OESTE])
        sur = int(self.walls[Direccion.SUR])
        este = int(self.walls[Direccion.ESTE])
        norte = int(self.walls[Direccion.NORTE])

        valor = oeste
        valor = (valor * 10) + sur
        valor = (valor * 10) + este
        valor = (valor * 10) + norte

        if valor == 0:
            return '0'
        if valor == 1:
            return '1'
        if valor == 10:
            return '2'
        if valor == 11:
            return '3'
        if valor == 100:
            return '4'
        if valor == 101:
            return '5'
        if valor == 110:
            return '6'
        if valor == 111:
            return '7'
        if valor == 1000:
            return '8'
        if valor == 1001:
            return '9'
        if valor == 1010:
            return 'A'
        if valor == 1011:
            return 'B'
        if valor == 1100:
            return 'C'
        if valor == 1101:
            return 'D'
        if valor == 1110:
            return 'E'
        if valor == 1111:
            return 'F'
        return '0'
