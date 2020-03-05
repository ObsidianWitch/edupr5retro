import sys
import pygame
from src.image import Image
from src.events import Events
from src.font import Font

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

        self.events = Events()

        self.fonts = list(
            Font(size) for size in range(18, 43, 6)
        )

    # Attributs

    ## ~~~{.python .prototype}
    ## fonts -> list<Font>
    ## ~~~
    ## Liste de polices de tailles ascendantes (18, 24, 30, 36 et 42).

    ## ~~~{.python .prototype}
    ## events -> Events
    ## ~~~

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

    ## ~~~{.python .prototype}
    ## loop(function instructions)
    ## ~~~
    ## Boucle principale du jeu.
    ##
    ## 1. récupère les nouveaux événements (`events.update()`)
    ## 2. exécute `instructions`
    ## 3. met à jour le contenu de la fenêtre (`update()`)
    def loop(self, instructions):
        while 1:
            self.events.update()
            if self.events.event(pygame.QUIT): sys.exit()

            instructions()

            self.update()
