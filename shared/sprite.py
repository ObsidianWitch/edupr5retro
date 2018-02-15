import os
import inspect

import numpy
import pygame

class Sprite(pygame.sprite.Sprite):
    project_path = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))),
        ".."
    )

    def __init__(self, images, position, animations = None,):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]

        self.animations = animations or {
            "DEFAULT": range(len(self.images)),
        }
        self.animation = next(iter(self.animations))

        self.rect = self.image.get_rect()
        self.rect.topleft = position

    @classmethod
    def from_images(
        cls, paths, position, colorkey = None,
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
    def from_ascii_sprites(
        cls, ascii_sprites, dictionary, position, colorkey = None,
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

    def update(self):
        #print(self.animation)
        frames = self.animations[self.animation]
        n_frames = len(frames)
        i = int(pygame.time.get_ticks() / 500) % n_frames
        self.image = self.images[frames[i]]

    def scale(self, ratio):
        new_images = []
        for img in self.images:
            old_size = self.image.get_size()
            new_size = (
                int(old_size[0] * ratio),
                int(old_size[1] * ratio)
            )
            new_images.append(
                pygame.transform.scale(img, new_size)
            )
        return new_images

    def scale_ip(self, ratio):
        self.images = self.scale(ratio)
        self.image = self.images[0]
