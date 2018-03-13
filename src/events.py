import pygame
class Events:
    # Constructeur

    ## Events() -> Events
    ## Gestion des événements.
    ##
    ## Un événement (`pygame.event.Event`) est constitué d'un type et
    ## d'attributs différents en fonction du type de l'événement.
    ## | type             | dict              |
    ## | ---------------- | ----------------- |
    ## | QUIT             | none              |
    ## | KEYDOWN          | unicode, key, mod |
    ## | KEYUP            | key, mod          |
    ## | MOUSEMOTION      | pos, rel, buttons |
    ## | MOUSEBUTTONUP    | pos, button       |
    ## | MOUSEBUTTONDOWN  | pos, button       |
    ## | USEREVENT        | code              |
    ##
    ## Les constantes se référant aux touches du clavier débutent par `K_`.
    ## Les constantes se référant aux boutons de la souris débutent par `M_`.
    ## se référer à la section Constantes de la documentation pour la liste
    ## complète.
    def __init__(self):
        pass

    # Méthodes

    ## update()
    ## Récupère les nouveaux événements disponibles. Cette méthode doit être
    ## appelée à chaque *frame* dans le jeu.
    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    ## event(int type) -> pygame.event.Event
    ## Cherche un événement du type spécifié. Retourne le premier événement
    ## trouvé ou `None`.
    def event(self, type):
        for e in self.events:
            if e.type == type: return e

    ## key_press(int key) -> bool
    ## Retourne si la touche du clavier spécifiée vient d'être enfoncée.
    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    ## key_hold(int key) -> bool
    ## Retourne si la touche du clavier spécifiée est maintenue enfoncée.
    def key_hold(self, key):
        return self.keyheld[key]

    ## key_release(int key) -> bool
    ## Retourne si la touche du clavier spécifiée vient d'être relâchée.
    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    ## mouse_press(int button = None) -> bool
    ## Retourne si un bouton de la souris vient d'être enfoncé.
    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## mouse_hold(int button = None) -> bool
    ## Retourne si un bouton de la souris est maintenu enfoncé.
    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    ## mouse_release(int button = None) -> bool
    ## Retourne si un bouton de la souris vient d'être relâché.
    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    ## mouse_pose() -> (x, y)
    ## Récupère la position de la souris.
    def mouse_pos(self):
        return pygame.mouse.get_pos()
