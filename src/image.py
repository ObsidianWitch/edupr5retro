import pygame
class Image:
    def __init__(self, size):
        self.pygsurface = pygame.Surface(size)
        self.rect = self.pygsurface.get_rect()

    @classmethod
    def from_pygsurface(cls, pygsurface):
        obj = Image((0, 0))
        obj.pygsurface = pygsurface
        obj.rect = obj.pygsurface.get_rect()
        return obj

    @classmethod
    def from_image(cls, path):
        return cls.from_pygsurface(pygame.image.load(path))

    @classmethod
    def from_array(cls, array):
        return cls.from_pygsurface(pygame.surfarray.make_surface(array))

    # Crée une copie superficielle de l'image actuelle. L'image actuelle et la
    # copie feront toutes deux référence à la même surface sous-jacente. Leurs
    # position et taille (`rect`) seront cependant indépendantes.
    def copy(self):
        obj = self.from_pygsurface(self.pygsurface)
        obj.rect = self.rect.copy()
        return obj

    # Crée une copie complète de l'image actuelle.
    def deepcopy(self):
        obj = self.from_pygsurface(self.pygsurface.copy())
        obj.rect = self.rect.copy()
        return obj

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

    # Dessine l'image `img` sur l'image actuelle. La position et la taille de
    # `img` sont déterminées à partir de `img.rect`. Le paramètre optionnel
    # `area` est un Rect et désigne quelle zone (plus petite) de `img` doit être
    # dessinée.
    def draw_image(self, img, area = None):
        self.pygsurface.blit(img.pygsurface, img.rect, area)
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
        self.rect = self.pygsurface.get_rect().move(self.rect.topleft)
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
