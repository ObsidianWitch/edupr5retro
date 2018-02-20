import pygame

from shared.sprite import Sprite

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
