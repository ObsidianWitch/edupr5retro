import pygame
class Surface:
    def __init__(self, size):
        self.pygsurface = pygame.Surface(size)

    @classmethod
    def from_pygsurface(cls, pygsurface):
        obj = Surface((0, 0))
        obj.pygsurface = pygsurface
        return obj

    @classmethod
    def from_image(cls, path):
        return cls.from_pygsurface(pygame.image.load(path))

    @classmethod
    def from_array(cls, array):
        return cls.from_pygsurface(pygame.surfarray.make_surface(array))

    def copy(self):
        return self.from_pygsurface(self.pygsurface.copy())

    @property
    def rect(self): return self.pygsurface.get_rect()

    @property
    def size(self): return self.rect.size

    @property
    def width(self): return self.rect.width

    @property
    def height(self): return self.rect.height

    def fill(self, color):
        self.pygsurface.fill(color)
        return self

    def colorkey(self, color):
        self.pygsurface.set_colorkey(color)
        return self

    def draw_surface(self, source, pos, area = None):
        if isinstance(source, Surface): source = source.pygsurface
        self.pygsurface.blit(source, pos, area)
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
        self.resize(size = (
                int(self.width * ratio),
                int(self.height * ratio),
        ))
        return self

    def rotate(self, angle):
        self.pygsurface = pygame.transform.rotate(self.pygsurface, angle)
        return self
