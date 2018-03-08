import pygame

class Window:
    def __init__(self, size, title, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        self.rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    @property
    def size(self): return self.rect.size

    @property
    def width(self): return self.rect.width

    @property
    def height(self): return self.rect.height

    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()
