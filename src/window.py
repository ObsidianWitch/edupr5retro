import pygame
from src.image import Image
class Window(Image):
    # Héritage

    ## > [Image](#classe-image)

    # constructeur

    ## ~~~{.python .prototype}
    ## Window(str title, 2-tuple size, int framerate = 30)
    ## ~~~
    ## Crée une fenêtre ayant pour titre `title` et de taille `size`. Le
    ## `framerate` est limité à 30 FPS par défaut.
    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

    # Méthodes de classe

    ## ~~~{.python .prototype}
    ## time() -> int
    ## ~~~
    ## Retourne le temps en millisecondes qui s'est écoulé depuis
    ## l'initialisation d'une fenêtre.
    @classmethod
    def time(cls): return pygame.time.get_ticks()

    # Méthodes

    ## ~~~{.python .prototype}
    ## cursor(bool enable)
    ## ~~~
    ## Active ou désactive le curseur. Par défaut, le curseur est activé.
    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    ## ~~~{.python .prototype}
    ## update()
    ## ~~~
    ## Met à jour le contenu de la fenêtre et limite le framerate.
    ## Cette méthode doit être appelée à chaque itération de la boucle
    ## principale du jeu.
    def update(self):
        self.clock.tick(self.framerate)
        pygame.display.flip()
