import collections
import pygame

from shared.sprite import Sprite
from shared.timer  import Timer

class Animation:
    def __init__(self, frames, loop = True):
        self.frames = frames
        self.loop   = loop

class Animations:
    @property
    def frame(self):
        i = self.timer.elapsed % len(self.current.frames)
        if self.finished: i = self.last_frame
        return self.current.frames[i]

    @property
    def last_frame(self): return (len(self.current.frames) - 1)

    @property
    def finished(self): return (not self.current.loop and self.timer.finished)

    def __init__(self, data, period):
        self.data = data
        self.period = period
        self.start(name = next(iter(self.data)))

    def set(self, name):
        self.current = self.data[name]

    def start(self, name):
        self.set(name)
        self.timer = Timer(
            end    = self.last_frame,
            period = self.period
        )

class AnimatedSprite(Sprite):
    def __init__(self, images, animations, position = (0, 0)):
        Sprite.__init__(self, images[0], position)
        self.images = images
        self.animations = animations

    @classmethod
    def from_path(cls, paths, animations, position = (0, 0)):
        images = cls.path_to_images(paths)
        return cls(images, animations, position)

    @classmethod
    def from_ascii(cls, txts, dictionary, animations, position = (0, 0)):
        images = cls.ascii_to_images(txts, dictionary)
        return cls(images, animations, position)

    @classmethod
    def from_spritesheet(
        cls, path, sprite_size, discard_color, animations,
        position = (0, 0)
    ):
        images = cls.spritesheet_to_images(path, sprite_size, discard_color)
        return cls(images, animations, position)

    @classmethod
    def spritesheet_to_images(cls, path, sprite_size, discard_color):
        spritesheet = cls.path_to_image(path)

        images = []
        for y in range(spritesheet.get_height() // sprite_size[1]):
            for x in range(spritesheet.get_width() // sprite_size[0]):
                img = spritesheet.subsurface(pygame.Rect(
                    x * sprite_size[0], # x
                    y * sprite_size[1], # y
                    sprite_size[0],     # width
                    sprite_size[1],     # height
                ))
                if img.get_at((0, 0)) == discard_color: break
                images.append(img)
        return images

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)
