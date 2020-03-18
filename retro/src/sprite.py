from __future__ import annotations
import typing as typ
import pygame
from src.image import Image

class Group(list):
    def __init__(self, *args: Sprite) -> None:
        list.__init__(self, args)
        for e in args: e.groups.append(self)

    def append(self, e: Sprite) -> None:
        list.append(self, e)
        e.groups.append(self)

    def update(self, *args: typ.Any, **kwargs: typ.Any) -> None:
        for e in self: e.update(*args, **kwargs)

    def draw(self, surface: Image) -> None:
        for e in self: e.draw(surface)

class Sprite:
    def __init__(self, image: Image) -> None:
        self.image = image
        self.rect = self.image.rect()
        self.groups: typ.List[Group] = []

    @classmethod
    def from_path(cls, path):
        return cls(Image.from_path(path))

    @classmethod
    def from_ascii(cls, txt, dictionary):
        return cls(Image.from_ascii(txt, dictionary))

    def flip(self, xflip = False, yflip = False):
        self.image.flip(xflip, yflip)

    def scale(self, ratio):
        self.image.scale(ratio)
        newrect = self.image.rect()
        newrect.move_ip(self.rect.topleft)
        self.rect = newrect

    def colorkey(self, color):
        self.image.colorkey(color)

    def kill(self) -> None:
        for g in self.groups: g.remove(self)
        self.groups = []

    # Update the sprite. DOes not do anything by default. Should be redefined.
    # Note: this method is called by `Group.update()`.
    def update(self) -> None:
        pass

    # Draw the sprite on the specified `image` at `self.rect.topleft`.
    def draw(self, image: Image) -> None:
        image.draw_img(self.image, self.rect.topleft)

class Counter:
    # A counter counts from 0 to `end`. Its value is incremented periodically
    # (`period`). By default the counter does not end (`end = 0`) and is
    # incremented every 1000 ms (`period = 1000`).
    def __init__(self, end: int = 0, period: int = 1000) -> None:
        self.end = end
        self.period = period
        self.restart()

    @property
    def elapsed(self) -> int:
        return (pygame.time.get_ticks() - self.t0) // self.period

    @property
    def remaining(self) -> int:
        return (self.end - self.elapsed)

    @property
    def finished(self) -> bool:
        return (self.elapsed >= self.end)

    def restart(self) -> None:
        self.t0 = pygame.time.get_ticks()

class Animations(typ.Dict[str, typ.Sequence[int]]):
    # Animations are stored as entries in this dictionary. Each entry map a name
    # to frames. Frames are represented by a list of indexes. Each index
    # references an image stored somewhere else. `period` specifies the time
    # necessary in milliseconds to switch to the next frame. By default, the
    # first animation defined in `self` is started.
    #
    # # Example
    # animations = retro.Animations(
    #     period = 100,
    #     WALK_L = range(0, 8),
    #     WALK_R = range(0 + 133, 8 + 133),
    #     FALL_L = range(8, 12),
    #     FALL_R = range(8 + 133, 12 + 133),
    #     ...
    # )
    def __init__(self, period: int, **kwargs: typ.Sequence[int]) -> None:
        dict.__init__(self, **kwargs)
        self.period = period
        if len(self) > 0:
            self.start(name = next(iter(self)))

    # Return the currently played frame's index.
    @property
    def frame(self) -> int:
        i = self.counter.elapsed % len(self.current)
        return self.current[i]

    # Return whether the animation has finished at least once.
    @property
    def finished(self) -> bool:
        return self.counter.finished

    # Sets the animation to play by specifying its `name`.
    def set(self, name: str) -> None:
        self.current = self[name]

    # Specify the animation to play by its `name` and starts it.
    def start(self, name: str) -> None:
        self.set(name)
        self.counter = Counter(
            end    = len(self.current),
            period = self.period,
        )

class AnimatedSprite(Sprite):
    def __init__(self, images: typ.List[Image], animations: Animations) -> None:
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
        images = Image.from_spritesheet(
            path, sprite_size, discard_color
        )
        images = list(itertools.chain(*images))
        return cls(images, animations)

    def scale(self, ratio):
        self.images = [img.scale(ratio) for img in self.images]
        self.image = self.images[0]
        newrect = self.image.rect()
        newrect.move_ip(self.rect.topleft)
        self.rect = newrect

    def flip(self, xflip = False, yflip = False):
        self.images = [img.flip(xflip, yflip) for img in self.images]
        self.image  = self.images[0]

    def colorkey(self, color):
        for img in self.images: img.colorkey(color)

    # Sets the current `self.image` as the current frame of the animation.
    def update(self) -> None:
        self.image = self.images[self.animations.frame]
