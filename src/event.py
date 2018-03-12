import pygame
class Event:
    # gestion des événements
    # Event() -> Event
    def __init__(self):
        pass

    # Récupère les nouveaux événements disponibles. Cette méthode doit être
    # appelée à chaque *frame* dans le jeu.
    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    # Cherche un événement du type spécifié.
    # Un événement (pygame.event.Event) est constitué d'un type et d'un
    # dictionnaire contenant des informations supplémentaires.
    # | type             | dict              |
    # | ---------------- | ----------------- |
    # | QUIT             | none              |
    # | KEYDOWN          | unicode, key, mod |
    # | KEYUP            | key, mod          |
    # | MOUSEMOTION      | pos, rel, buttons |
    # | MOUSEBUTTONUP    | pos, button       |
    # | MOUSEBUTTONDOWN  | pos, button       |
    # | USEREVENT        | code              |
    # **type**: `int`, type de l'événement
    # **returns**: `pygame.event.Event`, le premier événement trouvé, `None`
    # sinon.
    def event(self, type):
        for e in self.events:
            if e.type == type: return e

    # Cherche si la touche du clavier spécifiée vient d'être enfoncée.
    # **key**: `int`, touche du clavier (constantes `K_*`)
    # **returns**: `pygame.event.Event`, le premier événement trouvé, `None`
    # sinon.
    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return e

    # Cherche si la touche du clavier spécifiée est maintenue enfoncée.
    # **key**: `int`, touche du clavier (constantes `K_*`)
    # **returns**: `bool`, True si la touche est maintenue, False sinon.
    def key_hold(self, key):
        return self.keyheld[key]

    # Cherche si la touche du clavier spécifiée vient d'être relâchée.
    # **key**: `int`, touche du clavier (constantes `K_*`)
    # **returns**: `pygame.event.Event`, le premier événement trouvé, `None`
    # sinon.
    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return e

    # Cherche si un bouton de la souris vient d'être enfoncé.
    # **button**: `int`, bouton de la souris (constantes `M_*`), ou None
    # **returns**: `pygame.event.Event`, le premier événement trouvé, `None`
    # sinon.
    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return e
                elif e.button == button: return e

    # Cherche si un bouton de la souris est maintenu enfoncé.
    # **button**: `int`, bouton de la souris (constantes `M_*`), ou None
    # **returns**: `bool`, True si un bouton est maintenu, False sinon.
    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return self.mouseheld
            else: return self.mouseheld[button - 1]

    # Cherche si un bouton de la souris vient d'être relâché.
    # **button**: `int`, bouton de la souris (constantes `M_*`), ou None
    # **returns**: `pygame.event.Event`, le premier événement trouvé, `None`
    # sinon.
    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return e
                elif e.button == button: return e

    # Récupère la position de la souris.
    # **returns: `tuple (int x, int y)`, position de la souris
    def mouse_pos(self):
        return pygame.mouse.get_pos()
