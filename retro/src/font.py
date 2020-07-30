import pygame
from retro.src.constants import *
from retro.src.image import Image

class Font:
    def __init__(self, size):
        self.pygfont = pygame.font.SysFont(None, size)

    def render(self, text, antialias = True, color = BLACK, bgcolor = None):
        return Image(self.pygfont.render(text, antialias, color, bgcolor))
