from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationInfo, model_validator
from typing import Tuple
import pygame
import random
class Map(BaseModel):
    #He puesto esta restriccion partiendo de la base que las dimensiones incluyen las paredes de los bordes
    WIDTH: int = Field(gt=3)
    HEIGHT: int = Field(gt=3)
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str = Field(pattern=r".*\.txt$")
    PERFECT: bool
    grid: list[list[int]] = []
    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def comprobar_coordenadas(cls, v):
        if isinstance(v, str):
            try:
                x, y = map(int, v.split(",", 1))
                return (x, y)
            except Exception:
                raise ValueError("El dato debe contener cordenadas x,y")
    
    @field_validator('ENTRY', 'EXIT')
    @classmethod
    def validacion_datos(cls, v, info: ValidationInfo):
        w = info.data.get('WIDTH')
        h = info.data.get('HEIGHT')
        if (w and h):
            x, y = v
            if not(1 <= x < w and 1 <= y < h):
                raise ValueError(f"Coordenada {v} fuera de los limites{x},{y}")
        return v
    
    @model_validator(mode='after')
    def iniciando_grid(self):
        self.grid = [[1 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        #self.grid[self.ENTRY[1]][self.ENTRY[0]] = 2
        #self.grid[self.EXIT[1]][self.EXIT[0]] = 2
        return self

    def celda_valida(self, x, y):
        return 1 <= x < self.WIDTH-1 and 1 <= y < self.HEIGHT-1

    def backtracking(self, x, y):
        if self.grid[y][x] != 2:
            self.grid[y][x] = 0
        direcciones = [(0,2), (0,-2), (2,0), (-2,0)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            paredx, paredy = x + (dx//2), y + (dy//2)
            if self.celda_valida(nx, ny):
                if self.grid[ny][nx] == 1:
                    self.grid[ny][nx] = 0
                    self.grid[paredy][paredx] = 0
                    self.backtracking(nx, ny)
        

    def draw_map(self, screen: pygame.Surface, dimension: int):
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if self.grid[j][i] == 1:
                    pygame.draw.rect(screen, (25,25,166), (i*dimension, j*dimension, dimension, dimension))
                elif self.grid[j][i] == 2:
                    pygame.draw.rect(screen, (0,255,0), (i*dimension, j*dimension, dimension, dimension))
                else:
                    pygame.draw.rect(screen, (0,0,0), (i*dimension, j*dimension, dimension, dimension))
    
    def render(self, dimension, screen):
        self.backtracking(self.ENTRY[0],self.ENTRY[1])
        self.draw_map(screen, dimension)
        

    