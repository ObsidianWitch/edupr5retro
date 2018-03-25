import itertools
import include.retro as retro

class Sprite(retro.Sprite):
    @classmethod
    def from_path(cls, path):
        return cls(retro.Image.from_path(path))

    @classmethod
    def from_ascii(cls, txt, dictionary):
        return cls(retro.Image.from_ascii(txt, dictionary))

    def flip(self, xflip = False, yflip = False):
        self.image.flip(xflip, yflip)

    def scale(self, ratio):
        self.image.scale(ratio)
        self.rect = self.image.rect().move(self.rect.topleft)

    def colorkey(self, color):
        self.image.colorkey(color)

class AnimatedSprite(retro.AnimatedSprite):
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
