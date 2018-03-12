import pygame
from src.image import Image
class Window(Image):
    # Window(str title, tuple size, int framerate = 30)
    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    # time() -> int
    # Renvoie le temps en millisecondes qui s'est écoulé depuis l'initialisation
    # d'une fenêtre.
    @classmethod
    def time(cls): return pygame.time.get_ticks()

    # cursor(bool enable)
    # Active ou désactive le curseur.
    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    # update()
    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()
