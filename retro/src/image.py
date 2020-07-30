import pygame
import numpy
from pathlib import Path

class Image:
    def __init__(self, *args, **kwargs):
        arg = args[0]
        if isinstance(arg, Image):
            self.pygsurface = arg.pygsurface.copy()
        elif isinstance(arg, pygame.Surface):
            self.pygsurface = arg
        elif isinstance(arg, Path):
            self.__init__(pygame.image.load(str(arg)))
        else:
            self.__init__(pygame.Surface(*args, *kwargs))

    def copy(self):
        return self.__class__(self)

    def subimage(self, area):
        return self.__class__(self.pygsurface.subsurface(area))

    def rect(self):
        return self.pygsurface.get_rect()

    def __getitem__(self, pos):
        return self.pygsurface.get_at(pos)

    def __setitem__(self, pos, color):
        self.pygsurface.set_at(pos, color)

    def fill(self, color):
        self.pygsurface.fill(color)

    def draw_img(self, img, pos, area = None):
        self.pygsurface.blit(img.pygsurface, pos, area)

    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)

    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)

    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)

    def flip(self, x, y):
        self.pygsurface = pygame.transform.flip(self.pygsurface, x, y)

    def resize(self, size):
        self.pygsurface = pygame.transform.scale(self.pygsurface, size)

    def scale(self, ratio):
        self.resize((
            int(self.rect().w * ratio),
            int(self.rect().h * ratio),
        ))

    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)

    def __eq__(self, other):
        return numpy.array_equal(
            pygame.surfarray.pixels3d(self.pygsurface),
            pygame.surfarray.pixels3d(other.pygsurface)
        )

    def save(self, out):
        pygame.image.save(self.pygsurface, out)
