from __future__ import annotations
import itertools
import pygame
import numpy
import typing as typ
from retro.src.constants import *
from pygame import Rect

class Image:
    def __init__(self, arg: typ.Any) -> None:
        if isinstance(arg, Image):
            self.pygsurface: pygame.Surface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        elif isinstance(arg, typ.Sequence):
            Image.__init__(self, pygame.Surface(arg))
        else:
            raise NotImplementedError

    @classmethod
    def from_path(cls, path: str) -> Image:
        return cls(pygame.image.load(path))

    @classmethod
    def from_array(cls, array: numpy.ndarray) -> Image:
        return cls(pygame.surfarray.make_surface(array))

    # Load a spritesheet image from its `path` and cut it in subimages of size
    # `sprite_size`. Subimages containing the `discard_color` color at their
    # topleft corner are discarded. Return a list containg a list of subimages
    # for each line of the spritesheet.
    @classmethod
    def from_spritesheet(cls,
        path: str, sprite_size: typ.Tuple[int, int], discard_color: pygame.Color
    ) -> typ.List[Image]:
        spritesheet = cls.from_path(path)

        images = []
        for y in range(spritesheet.rect().h // sprite_size[1]):
            line = []
            for x in range(spritesheet.rect().w // sprite_size[0]):
                img = spritesheet.subimage(Rect(
                    x * sprite_size[0], # x
                    y * sprite_size[1], # y
                    sprite_size[0],     # width
                    sprite_size[1],     # height
                ))
                if img[0, 0] == discard_color: break
                line.append(img)
            images.append(line)

        return list(itertools.chain(*images))

    def copy(self) -> Image:
        return self.__class__(self)

    # Create a new Image that references its parent. Modifications to either
    # images will effect each other. `area` is the zone to extract from `self`.
    def subimage(self, area: Rect) -> Image:
        return self.__class__(self.pygsurface.subsurface(area))

    # Return a new rectangle at (0, 0) covering the entire image.
    def rect(self) -> Rect:
        return Rect(*self.pygsurface.get_rect())

    def __getitem__(self, pos: typ.Tuple[int, int]) -> pygame.Color:
        return self.pygsurface.get_at(pos)

    def __setitem__(self,
        pos: typ.Tuple[int, int], color: pygame.Color
    ) -> None:
        self.pygsurface.set_at(pos, color)

    # Set the current transparent color key for this image.
    def colorkey(self, color: pygame.Color) -> Image:
        self.pygsurface.set_colorkey(color)
        return self

    def fill(self, color: pygame.Color) -> Image:
        self.pygsurface.fill(color)
        return self

    # Draw `img` onto `self` at `pos`. An optional `area` can be specified can
    # be passed to select a smaller portion of `img` to draw.
    def draw_img(self,
        img: Image, pos: typ.Tuple[int, int], area: typ.Optional[Rect] = None
    ) -> Image:
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    def draw_rect(self,
        color: pygame.Color, rect: Rect, width: int = 0
    ) -> Image:
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    def draw_circle(self,
        color: pygame.Color, center: typ.Tuple[int, int], radius: int,
        width: int = 0
    ) -> Image:
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    def draw_line(self,
        color: pygame.Color, start_pos: typ.Tuple[int, int],
        end_pos: typ.Tuple[int, int], width: int = 1
    ) -> Image:
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    def flip(self, x: bool, y: bool) -> Image:
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    def resize(self, size: typ.Tuple[int, int]) -> Image:
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    def scale(self, ratio: float) -> Image:
        self.resize(size = (
                int(self.rect().w * ratio),
                int(self.rect().h * ratio),
        ))
        return self

    def rotate(self, angle: int) -> Image:
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self

    def __eq__(self, other):
        return numpy.array_equal(
            pygame.surfarray.pixels3d(self.pygsurface),
            pygame.surfarray.pixels3d(other.pygsurface)
        )

    def save(self, out):
        pygame.image.save(self.pygsurface, out)
