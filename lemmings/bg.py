import pygame

from lemmings.common import asset_path

class BG:
    def __init__(self):
        self.original = pygame.image.load(asset_path("map.png"))
        self.current  = self.original.copy()

    def clear(self):
        self.current.blit(self.original, (0, 0))
