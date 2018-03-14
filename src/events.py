import pygame
class Events:
    # Constructeur

    ## ~~~{.python .prototype}
    ## Events() -> Events
    ## ~~~
    ## Gestion de la file d'événements, de la souris et du clavier.
    ##
    ## Un événement ([`pygame.event.Event`](https://www.pygame.org/docs/ref/event.html#pygame.event.Event))
    ## est constitué d'un type et d'attributs différents en fonction du type de
    ## l'événement. Si vous souhaitez obtenir plus de détails, veuillez vous
    ## référer à la documentation du module
    ## [pygame.event](https://www.pygame.org/docs/ref/event.html).
    ##
    ## Les constantes des touches du clavier débutent par `K_`.
    ## Les constantes des boutons de la souris débutent par `M_`.
    ## Se référer à la section [Constantes](#constantes) de la documentation.
    def __init__(self):
        pass

    # Méthodes

    ## ~~~{.python .prototype}
    ## update()
    ## ~~~
    ## Récupère les nouveaux événements disponibles. Cette méthode doit être
    ## appelée à chaque *frame* dans le jeu.
    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    ## ~~~{.python .prototype}
    ## event(int type) -> pygame.event.Event
    ## ~~~
    ## Cherche un événement du type spécifié. Retourne le premier événement
    ## trouvé ou `None`.
    def event(self, type):
        for e in self.events:
            if e.type == type: return e

    ## ~~~{.python .prototype}
    ## key_press(int key) -> bool
    ## ~~~
    ## Retourne si la touche du clavier spécifiée vient d'être enfoncée.
    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    ## ~~~{.python .prototype}
    ## key_hold(int key) -> bool
    ## ~~~
    ## Retourne si la touche du clavier spécifiée est maintenue enfoncée.
    def key_hold(self, key):
        return self.keyheld[key]

    ## ~~~{.python .prototype}
    ## key_release(int key) -> bool
    ## ~~~
    ## Retourne si la touche du clavier spécifiée vient d'être relâchée.
    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_press(int button = None) -> bool
    ## ~~~
    ## Retourne si un bouton de la souris vient d'être enfoncé.
    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_hold(int button = None) -> bool
    ## ~~~
    ## Retourne si un bouton de la souris est maintenu enfoncé.
    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    ## ~~~{.python .prototype}
    ## mouse_release(int button = None) -> bool
    ## ~~~
    ## Retourne si un bouton de la souris vient d'être relâché.
    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_pose() -> 2-tuple
    ## ~~~
    ## Récupère la position de la souris.
    def mouse_pos(self):
        return pygame.mouse.get_pos()
