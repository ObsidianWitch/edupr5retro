import pygame
from src.image import Image

class Group(list):
    def __init__(self, *args):
        list.__init__(self, args)
        for e in args: e.groups.append(self)

    def append(self, e):
        list.append(self, e)
        e.groups.append(self)

    def update(self, *args):
        for e in self:
            if args: e.update(args)
            else:    e.update()

    def draw(self, surface):
        for e in self: e.draw(surface)

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.rect()
        self.groups = []

    def kill(self):
        for g in self.groups: g.remove(self)
        self.groups = []

    def update(self): pass

    def draw(self, image): image.draw_img(self.image, self.rect)

class Timer:
    def __init__(self, end = 0, period = 1000):
        self.end = end
        self.period = period
        self.restart()

    @property
    def time(self): return (pygame.time.get_ticks() // self.period)

    @property
    def elapsed(self): return (self.time - self.t0)

    @property
    def remaining(self): return (self.end - self.elapsed)

    @property
    def finished(self): return (self.elapsed >= self.end)

    def restart(self): self.t0 = self.time

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

    def update(self): self.image = self.images[self.animations.frame]
