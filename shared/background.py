import pygame

from shared.image import Image

class Background:
    def __init__(self, path):
        self.original = Image.from_path(path)
        self.current  = self.original.copy()
        self.rect = self.original.get_rect()

    def clear(self):
        self.current.blit(self.original, (0, 0))
