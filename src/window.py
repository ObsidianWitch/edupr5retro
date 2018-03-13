import pygame
from src.image import Image
class Window(Image):
    # constructeur

    ## Window(str title, tuple size, int framerate = 30)
    ## Crée une fenêtre.
    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    # Méthodes de classe

    ## time() -> int
    ## Retourne le temps en millisecondes qui s'est écoulé depuis
    ## l'initialisation d'une fenêtre.
    @classmethod
    def time(cls): return pygame.time.get_ticks()

    # Méthodes

    ## cursor(bool enable)
    ## Active ou désactive le curseur.
    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    ## update()
    ## Met à jour le contenu de la fenêtre et limite le framerate.
    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()
