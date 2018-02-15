import os
import inspect

import numpy
import pygame

class Sprite(pygame.sprite.Sprite):
    project_path = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))),
        ".."
    )

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    @classmethod
    def from_image(cls, image_path, position, colorkey = None):
        image = pygame.image.load(
            os.path.join(cls.project_path, image_path)
        )

        if colorkey: image.set_colorkey(colorkey)

        return cls(image, position)

    def scale(self, ratio):
        old_size = self.image.get_size()
        new_size = (
            int(old_size[0] * ratio),
            int(old_size[1] * ratio)
        )
        self.image = pygame.transform.scale(self.image, new_size)
