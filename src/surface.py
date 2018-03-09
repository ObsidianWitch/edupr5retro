class Surface:
    def __init__(self, size):
        self.pygsurface = pygame.Surface(size)

    @property
    def rect(self): return self.pygsurface.get_rect()

    @property
    def size(self): return self.rect.size

    @property
    def width(self): return self.rect.width

    @property
    def height(self): return self.rect.height

    def copy(self):
        obj = cls((0, 0))
        obj.pygsurface = self.pygsurface.copy()
        return obj

    def fill(self, color):
        self.pygsurface.fill(color)

    def draw_surface(self, source, pos, area = None):
        self.pygsurface.blit(source, pos, area)

    def draw_rect(self, color, rect, width = 0):
        pygame.draw.rect(self.pygsurface, color, rect, width)

    def draw_circle(self, color, center, radius, width = 0):
        pygame.draw.circle(self.pygsurface, color, center, radius, width)

    def draw_line(self, color, start_pos, end_pos, width = 1):
        pygame.draw.line(self.pygsurface, color, start_pos, end_pos, width)
