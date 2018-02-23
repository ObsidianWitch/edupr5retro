import pygame

import shared.transform
from shared.image import Image

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, position = (0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.move_ip(position)

    @classmethod
    def from_path(cls, path, position = (0, 0)): return cls(
        image    = Image.from_path(path),
        position = position,
    )

    @classmethod
    def from_ascii(cls, txt, dictionary, position = (0, 0)): return cls(
        image    = Image.from_ascii(txt, dictionary),
        position = position
    )

    @property
    def bounding_rect(self): return (
        self.image
            .get_bounding_rect()
            .move(self.rect.topleft)
    )

    def scale(self, ratio):
        self.image = shared.transform.scale(self.image, ratio)
        self.rect  = self.image.get_rect()

    def flip(self, xflip = False, yflip = False):
        self.image = pygame.transform.flip(self.image, xflip, yflip)

    def colorkey(self, color):
        self.image.set_colorkey(color)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
