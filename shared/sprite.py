import os
import inspect

import numpy
import pygame

class Sprite(pygame.sprite.Sprite):
    project_path = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))),
        ".."
    )

    def __init__(self, images, position = (0, 0), animations = None):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]

        self.animations = animations or {
            "DEFAULT": range(len(self.images)),
        }
        self.animation = next(iter(self.animations))

        self.rect = self.image.get_rect()
        self.rect.move_ip(position)

    @classmethod
    def from_paths(
        cls, paths, position = (0, 0), colorkey = None,
        animations = None,
    ):
        images = []
        for path in paths:
            image = pygame.image.load(
                os.path.join(cls.project_path, path)
            )
            if colorkey: image.set_colorkey(colorkey)
            images.append(image)

        return cls(images, position, animations)

    @classmethod
    def from_ascii(
        cls, ascii_sprites, dictionary, position = (0, 0), colorkey = None,
        animations = None,
    ):
        images = []
        for ascii_sprite in ascii_sprites:
            image = cls.ascii_to_image(ascii_sprite, dictionary)
            if colorkey: image.set_colorkey(colorkey)
            images.append(image)

        return cls(images, position, animations)

    @classmethod
    def ascii_to_image(cls, ascii_sprite, dictionary):
        height = len(ascii_sprite)
        width  = len(ascii_sprite[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = ascii_sprite[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return pygame.surfarray.make_surface(rgb_sprite)

    def scale(self, ratio):
        self.rect.size = (
            int(self.rect.width * ratio),
            int(self.rect.height * ratio)
        )

        new_images = []
        for img in self.images: new_images.append(
            pygame.transform.scale(img, self.rect.size)
        )
        return new_images

    def scale_ip(self, ratio):
        self.images = self.scale(ratio)
        self.image  = self.images[0]

    def update(self):
        frames = self.animations[self.animation]
        i = (pygame.time.get_ticks() // 500) % len(frames)
        self.image = self.images[frames[i]]
