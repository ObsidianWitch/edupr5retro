import pygame
import numpy
import typing as T
from retro.src.constants import *

class Image:
    def __init__(self, arg):
        if isinstance(arg, Image):
            self.pygsurface: pygame.Surface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        elif isinstance(arg, T.Sequence):
            Image.__init__(self, pygame.Surface(arg))
        else:
            raise NotImplementedError

    @classmethod
    def from_path(cls, path):
        return cls(pygame.image.load(path))

    @classmethod
    def from_array(cls, array):
        return cls(pygame.surfarray.make_surface(array))

    def copy(self):
        return self.__class__(self)

    # Create a new Image that references its parent. Modifications to either
    # images will effect each other. `area` is the zone to extract from `self`.
    def subimage(self, area):
        return self.__class__(self.pygsurface.subsurface(area))

    # Return a new rectangle at (0, 0) covering the entire image.
    def rect(self):
        return self.pygsurface.get_rect()

    def __getitem__(self, pos):
        return self.pygsurface.get_at(pos)

    def __setitem__(self, pos, color):
        self.pygsurface.set_at(pos, color)

    # Set the current transparent color key for this image.
    def colorkey(self, color):
        self.pygsurface.set_colorkey(color)
        return self

    def fill(self, color):
        self.pygsurface.fill(color)
        return self

    # Draw `img` onto `self` at `pos`. An optional `area` can be specified can
    # be passed to select a smaller portion of `img` to draw.
    def draw_img(self, img, pos, area = None):
        self.pygsurface.blit(img.pygsurface, pos, area)
        return self

    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)
        return self

    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)
        return self

    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
        return self

    def flip(self, x, y):
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)
        return self

    def resize(self, size):
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)
        return self

    def scale(self, ratio):
        self.resize((
            int(self.rect().w * ratio),
            int(self.rect().h * ratio),
        ))
        return self

    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self

    def __eq__(self, other):
        return numpy.array_equal(
            pygame.surfarray.pixels3d(self.pygsurface),
            pygame.surfarray.pixels3d(other.pygsurface)
        )

    def save(self, out):
        pygame.image.save(self.pygsurface, out)
