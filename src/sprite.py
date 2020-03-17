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

    def kill(self) -> None:
        for g in self.groups: g.remove(self)
        self.groups = []

    # Update the sprite. DOes not do anything by default. Should be redefined.
    # Note: this method is called by `Group.update()`.
    def update(self) -> None:
        pass

    # Draw the sprite on the specified `image` at `self.rect.lt`.
    def draw(self, image: Image) -> None:
        image.draw_img(self.image, self.rect.lt)

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

class Animations:
    # Animations are contained in `data`. Each entry map a name to frames.
    # Frames are represented by a list of indexes. Each index references an
    # image stored somewhere else. `period` specified the time necessary in
    # milliseconds to switch to the next frame. By default, the first animation
    # defined in `data` is started.
    #
    # # Example
    # animations = retro.Animations(
    #     data = {
    #         "WALK_L":  range(0, 8),
    #         "WALK_R":  range(0 + 133, 8 + 133),
    #         "FALL_L":  range(8, 12),
    #         "FALL_R":  range(8 + 133, 12 + 133),
    #         ...
    #     },
    #     period  = 100,
    # )
    def __init__(self,
        data: typ.Dict[str, typ.Sequence[int]], period: int
    ) -> None:
        self.data   = data
        self.period = period
        if len(data) > 0: self.start(name = next(iter(self.data)))

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
        self.current = self.data[name]

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

    # Sets the current `self.image` as the current frame of the animation.
    def update(self) -> None:
        self.image = self.images[self.animations.frame]
