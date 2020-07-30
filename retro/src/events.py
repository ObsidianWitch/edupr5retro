import pygame

class Events:
    # Retrieve new events. This method should be called each frame.
    def update(self):
        self.events = pygame.event.get()
        self.keyheld = pygame.key.get_pressed()
        self.mouseheld = pygame.mouse.get_pressed()

    # Returns the first event found of the specified `type`.
    def event(self, type):
        for e in self.events:
            if e.type == type: return e
        return None

    def key_press(self, key):
        for e in self.events:
            if (e.type == pygame.KEYDOWN) and (e.key == key): return True
        return False

    def key_hold(self, key):
        return self.keyheld[key]

    def key_release(self, key):
        for e in self.events:
            if (e.type == pygame.KEYUP) and (e.key == key): return True
        return False

    def mouse_press(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if button is None: return True
                elif e.button == button: return True
        return False

    def mouse_hold(self, button = None):
        if any(self.mouseheld):
            if button is None: return True
            else: return self.mouseheld[button - 1]
        return False

    def mouse_release(self, button = None):
        for e in self.events:
            if (e.type == pygame.MOUSEBUTTONUP):
                if button is None: return True
                elif e.button == button: return True
        return False

    def mouse_pos(self):
        return pygame.mouse.get_pos()
