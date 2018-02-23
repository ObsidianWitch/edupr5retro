import pygame

from shared.sprite import Sprite
from shared.image import Image
from shared.timer import Timer

class Animations:
    @property
    def frame(self):
        i = self.timer.elapsed % len(self.current)
        return self.current[i]

    @property
    def finished(self): return self.timer.finished

    def __init__(self, data, period):
        self.data   = data
        self.period = period
        self.start(name = next(iter(self.data)))

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
        self.rect.size = (
            int(self.rect.width * ratio),
            int(self.rect.height * ratio)
        )
        return [
            pygame.transform.scale(img, self.rect.size)
            for img in self.images
        ]

    def scale_ip(self, ratio):
        self.images = self.scale(ratio)
        self.image  = self.images[0]

    def flip(self, xflip = False, yflip = False): return [
        pygame.transform.flip(img, xflip, yflip)
        for img in self.images
    ]

    def flip_ip(self, xflip = False, yflip = False):
        self.images = self.flip(xflip, yflip)
        self.image  = self.images[0]

    def colorkey(self, color):
        for img in self.images: img.set_colorkey(color)

    def update(self):
        self.image = self.images[self.animations.frame]
