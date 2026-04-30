from enum import Enum
import random

class Direccion(Enum):
    NORTE = "N"
    SUR = "S"
    ESTE = "E"
    OESTE = "W"
    
OPUESTO = {
    Direccion.NORTE: Direccion.SUR,
    Direccion.SUR: Direccion.NORTE,
    Direccion.ESTE: Direccion.OESTE,
    Direccion.OESTE: Direccion.ESTE        
    }
MOVES = {
    Direccion.NORTE:(0,-1),
    Direccion.SUR:(0,1),
    Direccion.ESTE:(1,0),
    Direccion.OESTE:(-1,0)
}