import os, inspect

import pygame

class Sprite(pygame.sprite.Sprite):
    project_path = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))),
        ".."
    )

    def __init__(self, image_path, position, colorkey = None, scale = None):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(
            os.path.join(self.project_path, image_path)
        )

        if scale:
            new_size = self.image.get_size()
            new_size = (
                int(new_size[0] * scale),
                int(new_size[1] * scale)
            )
            self.image = pygame.transform.scale(self.image, new_size)

        if colorkey: self.image.set_colorkey(colorkey)

        self.rect = self.image.get_rect()
        self.rect.topleft = position
