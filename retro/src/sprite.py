import pygame
from retro.src.image import Image

class Group(list):
    def __init__(self, *args):
        list.__init__(self, args)
        for e in args:
            e.groups.append(self)

    def append(self, e):
        list.append(self, e)
        e.groups.append(self)

    def update(self, *args, **kwargs):
        for e in self: e.update(*args, **kwargs)

    def draw(self, surface):
        for e in self: e.draw(surface)

class Counter:
    # A Counter counts from 0 to `end`. Its value is incremented periodically
    # (`period`). By default the counter does not end (`end = 0`) and is
    # incremented every 1000 ms (`period = 1000`).
    def __init__(self, end = 0, period = 1000):
        self.end = end
        self.period = period
        self.restart()

    @property
    def elapsed(self):
        return (pygame.time.get_ticks() - self.t0) // self.period

    @property
    def remaining(self):
        return (self.end - self.elapsed)

    @property
    def finished(self):
        return (self.elapsed >= self.end)

    def restart(self):
        self.t0 = pygame.time.get_ticks()

class Animations(dict):

    # Animations are stored as entries in this dictionary. Each entry maps a
    # name to frame coordinates (row, col). Each tuple of coordinates references
    # a position in an image stored somewhere else. `period` specifies the time
    # necessary in milliseconds to switch to the next frame. By default, the
    # first animation defined in `self` is started.
    #
    # # Example
    # Animations(
    #     frame_size = (30, 30),
    #     period = 100,
    #     WALK_L = (range(0, 8), 0),
    #     WALK_R = (tuple(reversed(range(0, 8))), 11),
    #     ...
    # )
    def __init__(self, frame_size, period, **kwargs):
        dict.__init__(self, **kwargs)
        self.frame_size = frame_size
        self.period = period
        self.start(next(iter(self)))

    # Return the currently played frame's rect.
    @property
    def frame(self):
        i = self.counter.elapsed % len(self.current[0])
        return pygame.Rect(
            self.current[0][i] * self.frame_size[0],
            self.current[1]    * self.frame_size[1],
            *self.frame_size
        )

    # Return whether the animation has finished at least once.
    @property
    def finished(self):
        return self.counter.finished

    # Sets the animation to play by specifying its `name`.
    def set(self, name):
        self.current = self[name]

    # Specify the animation to play by its `name` and starts it.
    def start(self, name):
        self.set(name)
        self.counter = Counter(
            end    = len(self.current[0]),
            period = self.period,
        )

class Sprite:
    def __init__(self, image, animations = None):
        self.image = image
        self.rect = self.image.rect()
        self.groups: typ.List[Group] = []
        self.animations = animations
        if self.animations:
            self.rect.size = self.animations.frame_size

    @classmethod
    def from_path(cls, path):
        return cls(Image(path))

    @classmethod
    def from_spritesheet(cls, path, animations):
        return cls(Image(path), animations)

    # Remove `self` from all the `self.groups` it is in.
    def kill(self):
        for g in self.groups: g.remove(self)
        self.groups = []

    # Does nothing by default, should be overriden.
    # Note: this method is called by `Group.update()`.
    def update(self):
        pass

    # Draw the sprite's `self.image` on the specified `target` at
    # `self.rect.topleft` or `position` if specified. If `self.animations`
    # exists, the current frame is drawn instead. A smaller portion of the
    # image/frame can be drawn by specifying `area`.
    def draw(self, target, position = None, area = None):
        if self.animations and area:
            area = area.move(self.animations.frame.topleft)
            area = area.clip(self.animations.frame)
        elif self.animations:
            area = self.animations.frame

        position = position or self.rect.topleft

        target.draw_img(self.image, position, area)
