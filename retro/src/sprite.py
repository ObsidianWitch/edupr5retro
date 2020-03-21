from __future__ import annotations
import typing as typ
import pygame
from retro.src.image import Image

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

Animation = typ.Tuple[typ.Sequence[int], int]
class Animations(typ.Dict[str, Animation]):

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
    def __init__(self,
        frame_size: typ.Tuple[int, int], period: int, **kwargs: Animation,
    ) -> None:
        dict.__init__(self, **kwargs)
        self.frame_size = frame_size
        self.period = period
        self.start(next(iter(self)))

    # Return the currently played frame's rect.
    @property
    def frame(self) -> pygame.Rect:
        i = self.counter.elapsed % len(self.current[0])
        return pygame.Rect(
            self.current[0][i] * self.frame_size[0],
            self.current[1]    * self.frame_size[1],
            *self.frame_size
        )

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
            end    = len(self.current[0]),
            period = self.period,
        )

class Sprite:
    def __init__(self, image: Image, animations: Animations = None) -> None:
        self.image = image
        self.rect = self.image.rect()
        self.groups: typ.List[Group] = []
        self.animations = animations
        if self.animations:
            self.rect.size = self.animations.frame_size

    @classmethod
    def from_path(cls, path: str) -> Sprite:
        return cls(Image.from_path(path))

    @classmethod
    def from_spritesheet(cls, path: str, animations: Animations) -> Sprite:
        return cls(Image.from_path(path), animations)

    # Remove `self` from all the `self.groups` it is in.
    def kill(self) -> None:
        for g in self.groups: g.remove(self)
        self.groups = []

    # Does nothing by default, should be overriden.
    # Note: this method is called by `Group.update()`.
    def update(self) -> None:
        pass

    # Draw the sprite's `self.image` on the specified `target` at
    # `self.rect.topleft` or `position` if specified. If `self.animations`
    # exists, the current frame is drawn instead. A smaller portion of the
    # image/frame can be drawn by specifying `area`.
    def draw(self, target: Image, position: typ.Tuple[int, int] = None,
        area: pygame.Rect = None,
    ) -> None:
        if self.animations and area:
            area = area.move(self.animations.frame.topleft)
            area = area.clip(self.animations.frame)
        elif self.animations:
            area = self.animations.frame

        position = position or self.rect.topleft

        target.draw_img(self.image, position, area)
