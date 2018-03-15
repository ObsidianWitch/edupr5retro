import itertools
import include.retro as retro
from shared.sprite import Sprite
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
        if len(data) > 0: self.start(name = next(iter(self.data)))

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
    def __init__(self, images, animations):
        Sprite.__init__(self, images[0])
        self.images = images
        self.animations = animations

    @classmethod
    def from_path(cls, paths, animations):
        return cls(
            images     = [Sprite.from_path(p).image for p in paths],
            animations = animations,
        )

    @classmethod
    def from_ascii(cls, txts, dictionary, animations):
        return cls(
            images     = [Sprite.from_ascii(t, dictionary).image for t in txts],
            animations = animations,
        )

    @classmethod
    def from_spritesheet(cls, path, sprite_size, discard_color, animations):
        images = retro.Image.from_spritesheet(
            path, sprite_size, discard_color
        )
        images = list(itertools.chain(*images))
        return cls(images, animations)

    def scale(self, ratio):
        self.images = [img.scale(ratio) for img in self.images]
        self.image  = self.images[0]
        self.rect   = self.image.rect().move(self.rect.topleft)

    def flip(self, xflip = False, yflip = False):
        self.images = [img.flip(xflip, yflip) for img in self.images]
        self.image  = self.images[0]

    def colorkey(self, color):
        for img in self.images: img.colorkey(color)

    def update(self):
        self.image = self.images[self.animations.frame]
