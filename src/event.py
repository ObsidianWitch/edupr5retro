import pygame

class Event:
    @classmethod
    def update(cls):
        cls.events = pygame.event.get()
        cls.keyheld = pygame.key.get_pressed()
        cls.mouseheld = pygame.mouse.get_pressed()

    @classmethod
    def event(cls, type):
        for e in cls.events:
            if e.type == type: return e
        return False

    @classmethod
    def key_press(cls, key):
        for e in cls.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return e
        return False

    @classmethod
    def key_held(cls, key):
        return cls.keyheld[key]

    @classmethod
    def key_release(cls, key):
        for e in cls.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return e
        return False

    @classmethod
    def mouse_press(cls, button = None):
        for e in cls.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return e
                elif e.button == button: return e
        return False

    @classmethod
    def mouse_held(cls, button = None):
        if any(cls.mouseheld):
            if button is None: return cls.mouseheld
            else: return cls.mouseheld[button - 1]
        return False

    @classmethod
    def mouse_release(cls, button = None):
        for e in cls.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return e
                elif e.button == button: return e
        return False

    @classmethod
    def mouse_pos(cls):
        return pygame.mouse.get_pos()
