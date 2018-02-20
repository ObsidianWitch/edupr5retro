import os
import inspect
import numpy
import pygame

class Sprite(pygame.sprite.Sprite):
    project_path = os.path.join(
        os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))),
        ".."
    )

    def __init__(self, image, position = (0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.move_ip(position)

    @classmethod
    def from_path(cls, path, position = (0, 0)): return cls(
        image    = cls.path_to_image(path),
        position = position,
    )

    @classmethod
    def from_ascii(cls, txt, dictionary, position = (0, 0)): return cls(
        image    = cls.ascii_to_image(txt, dictionary),
        position = position
    )

    @classmethod
    def path_to_image(cls, path): return pygame.image.load(
        os.path.join(cls.project_path, path)
    )

    @classmethod
    def ascii_to_image(cls, txt, dictionary):
        height = len(txt)
        width  = len(txt[0])

        rgb_sprite = numpy.zeros((width, height, 3))
        for y, x in numpy.ndindex(height, width):
            c = txt[y][x]
            rgb_sprite[x,y] = dictionary[c]

        return pygame.surfarray.make_surface(rgb_sprite)

    @classmethod
    def path_to_images(cls, paths): return [
        cls.path_to_image(path) for path in paths
    ]

    @classmethod
    def ascii_to_images(cls, txts, dictionary): return [
        cls.ascii_to_image(txt, dictionary) for txt in txts
    ]

    def scale(self, ratio):
        self.rect.size = (
            int(self.rect.width * ratio),
            int(self.rect.height * ratio)
        )
        return pygame.transform.scale(self.image, self.rect.size)

    def scale_ip(self, ratio):
        self.image = self.scale(ratio)

    def flip(self, xflip = False, yflip = False):
        return pygame.transform.flip(self.image, xflip, yflip)

    def flip_ip(self, xflip = False, yflip = False):
        self.image = self.flip(xflip, yflip)

    def colorkey(self, color):
        self.image.set_colorkey(color)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class AnimatedSprite(Sprite):
    def __init__(self, images, position = (0, 0), animations = None):
        Sprite.__init__(self, images[0], position)
        self.images = images
        self.animations = animations or {
            "DEFAULT": range(len(self.images)),
        }
        self.animation = next(iter(self.animations))

    @classmethod
    def from_path(cls, paths, position = (0, 0), animations = None):
        images = cls.path_to_images(paths)
        return cls(images, position, animations)

    @classmethod
    def from_ascii(cls, txts, dictionary, position = (0, 0), animations = None):
        images = cls.ascii_to_images(txts, dictionary)
        return cls(images, position, animations)

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
        frames = self.animations[self.animation]
        i = (pygame.time.get_ticks() // 500) % len(frames)
        self.image = self.images[frames[i]]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
