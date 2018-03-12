import pygame
from src.constants import *
from src.image import Image
class Font:
    # Gestion des polices d'écriture.
    # Font(size) -> Font
    # **size**: `int`, traille de la police d'écriture.
    def __init__(self, size):
        self.font = pygame.font.SysFont(None, size)

    # Crée une Image avec le texte spécifié dessus.
    # **text**: texte
    # **antialias**: `bool`, lisse ou non la police d'écriture
    # **color**: `tuple (int r, int g, int b)`, couleur du texte
    # **bgcolor**: `tuple (int r, int g, int b)`, couleur de fond, transparent
    #              si None
    def render(self, text, antialias = False, color = BLACK, bgcolor = None):
        return Image(
            self.font.render(text, antialias, color, bgcolor)
        )
