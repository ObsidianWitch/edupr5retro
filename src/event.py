import pygame
class Event:
    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    def event(self, type):
        for e in self.events:
            if e.type == type: return e
        return False

    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return e
        return False

    def key_hold(self, key):
        return self.keyheld[key]

    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return e
        return False

    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return e
                elif e.button == button: return e
        return False

    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return self.mouseheld
            else: return self.mouseheld[button - 1]
        return False

    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return e
                elif e.button == button: return e
        return False

    def mouse_pos(self):
        return pygame.mouse.get_pos()
