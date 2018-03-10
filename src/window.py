import pygame
from src.surface import Surface
class Window(Surface):
    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        self.pygsurface = pygame.display.set_mode(size)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    # Renvoie le temps en millisecondes qui s'est écoulé depuis l'initialisation
    # d'une fenêtre.
    @classmethod
    def time(cls): return pygame.time.get_ticks()

    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()
