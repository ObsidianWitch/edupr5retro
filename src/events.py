import typing
import pygame

class Events:
    # Constructeur

    ## ~~~{.python .prototype}
    ## __init__(self) -> None
    ## ~~~
    ## Gestion de la file d'événements, de la souris et du clavier.
    ##
    ## Un événement ([`pygame.event.Event`](https://www.pygame.org/docs/ref/event.html#pygame.event.Event))
    ## est constitué d'un type et d'attributs différents en fonction du type de
    ## l'événement. Si vous souhaitez obtenir plus de détails, veuillez vous
    ## référer à la documentation du module
    ## [pygame.event](https://www.pygame.org/docs/ref/event.html).
    ## La liste des événements est disponible dans la section
    ## [Constantes](#événements).
    def __init__(self) -> None:
        pass

    # Méthodes

    ## ~~~{.python .prototype}
    ## update(self) -> None
    ## ~~~
    ## Récupère les nouveaux événements disponibles. Cette méthode doit être
    ## appelée à chaque *frame* dans le jeu.
    def update(self) -> None:
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    ## ~~~{.python .prototype}
    ## event(self, type: int) -> pygame.event.Event
    ## ~~~
    ## Cherche un événement du [`type`](#événements) spécifié.
    ## Retourne le premier événement trouvé ou `None`.
    def event(self, type: int) -> pygame.event.Event:
        for e in self.events:
            if e.type == type: return e

    ## ~~~{.python .prototype}
    ## key_press(self, key: int) -> bool
    ## ~~~
    ## Retourne si la [touche du clavier](#clavier) spécifiée vient d'être
    ## enfoncée.
    def key_press(self, key: int) -> bool:
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    ## ~~~{.python .prototype}
    ## key_hold(self, key: int) -> bool
    ## ~~~
    ## Retourne si la [touche du clavier](#clavier) spécifiée est maintenue
    ## enfoncée.
    def key_hold(self, key: int) -> bool:
        return self.keyheld[key]

    ## ~~~{.python .prototype}
    ## key_release(self, key: int) -> bool
    ## ~~~
    ## Retourne si la [touche du clavier](#clavier) spécifiée vient d'être
    ## relâchée.
    def key_release(self, key: int) -> bool:
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_press(self, button: int = None) -> bool
    ## ~~~
    ## Retourne si un [bouton de la souris](#souris) vient d'être enfoncé.
    def mouse_press(self, button: int = None) -> bool:
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_hold(self, button: int = None) -> bool
    ## ~~~
    ## Retourne si un [bouton de la souris](#souris) est maintenu enfoncé.
    def mouse_hold(self, button: int = None) -> bool:
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    ## ~~~{.python .prototype}
    ## mouse_release(self, button: int = None) -> bool
    ## ~~~
    ## Retourne si un [bouton de la souris](#souris) vient d'être relâché.
    def mouse_release(self, button: int = None) -> bool:
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## ~~~{.python .prototype}
    ## mouse_pos(self) -> typing.Tuple[int, int]
    ## ~~~
    ## Récupère la position de la souris.
    def mouse_pos(self) -> typing.Tuple[int, int]:
        return pygame.mouse.get_pos()
