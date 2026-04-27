from Boton import Boton
import pygame
class Menu():
    def __init__(self, screen_width, screen_height):
        centro_x = screen_width//2
        centro_y = screen_height//2
        self.botones = {
            "3D": Boton(centro_x-210, centro_y - 210, 140,56),
            "Pokemon": Boton(centro_x-210, centro_y-70,140,56),
            "None": Boton(centro_x-210, centro_y + 70,140,56)
        }
    
    def render(self, screen: pygame.Surface):
        screen.fill((50, 50, 50))
        for str, boton in self.botones.items():
            lista_frames = boton._animaciones[str]
            img = lista_frames[int(boton._frameActual)]
            screen.blit(img, boton._rect)