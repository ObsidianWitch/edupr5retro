import pygame

class Window:
    def __init__(self, size, title):
        pygame.init()
        pygame.mixer.quit()

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        self.rect = self.screen.get_rect()

    @property
    def size(self): return self.rect.size

    @property
    def width(self): return self.rect.width

    @property
    def height(self): return self.rect.height

    def cursor(self, enable):
        pygame.mouse.set_visible(enable)
