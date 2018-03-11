import pygame
from src.image import Image
class Font:
    def __init__(self, size):
        self.font = pygame.font.SysFont(None, size)

    # Crée une Image avec le texte spécifié dessus.
    def render(self, text, antialias = False, color = (0, 0, 0), bgcolor = None):
        return Image.from_pygsurface(
            self.font.render(text, antialias, color, bgcolor)
        )
