import pygame

from shared.image import Image
from lemmings.path import asset_path

class BG:
    def __init__(self, filename):
        self.original = Image.from_path(asset_path(filename))
        self.current  = self.original.copy()

    def clear(self):
        self.current.blit(self.original, (0, 0))
