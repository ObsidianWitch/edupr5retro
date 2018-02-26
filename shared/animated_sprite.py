import pygame

import shared.transform
from shared.sprite import Sprite
from shared.image import Image
from shared.timer import Timer

class Animations:
    # `data` must be a dictionary where the key is the name of one animation
    # and the value contains frames (a list containing indices each referencing
    # an image).
    # `period` corresponds to the time in ms needed to switch from one frame to
    # another.
    def __init__(self, data, period):
        self.data   = data
        self.period = period
        self.start(name = next(iter(self.data)))

    @property
    def frame(self):
        i = self.timer.elapsed % len(self.current)
        return self.current[i]

    @property
    def finished(self): return self.timer.finished

    def set(self, name):
        self.current = self.data[name]

    def start(self, name):
        self.set(name)
        self.timer = Timer(
            end    = len(self.current),
            period = self.period,
        )

class AnimatedSprite(Sprite):
    def __init__(self, images, animations, position = (0, 0)):
        Sprite.__init__(self, images[0], position)
        self.images = images
        self.animations = animations

    @classmethod
    def from_path(cls, paths, animations, position = (0, 0)):
        return cls(
            images     = Image.from_path_n(paths),
            animations = animations,
            position   = position,
        )

    @classmethod
    def from_ascii(cls, txts, dictionary, animations, position = (0, 0)):
        return cls(
            images     = Image.from_ascii_n(txts, dictionary),
            animations = animations,
            position   = position,
        )

    @classmethod
    def from_spritesheet(
        cls, path, sprite_size, discard_color, animations,
        position = (0, 0)
    ):
        return cls(
            images     = Image.from_spritesheet_n(
                path, sprite_size, discard_color
            ),
            animations = animations,
            position   = position,
        )

    def scale(self, ratio):
        self.images = shared.transform.scale_n(self.images, ratio)
        self.image  = self.images[0]
        self.rect   = self.image.get_rect().move(self.rect.topleft)

    def flip(self, xflip = False, yflip = False):
        self.images = shared.transform.flip_n(self.images, xflip, yflip)
        self.image  = self.images[0]

    def colorkey(self, color):
        for img in self.images: img.set_colorkey(color)

    def update(self):
        self.image = self.images[self.animations.frame]
