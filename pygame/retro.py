import sys
import time
import pygame

class Clock:
    def __init__(self, framerate):
        self.period = (1 / framerate)
        self.last_tick = time.time()

    def tick(self):
        delta = time.time() - self.last_tick
        if (delta < self.period): time.sleep(self.period - delta)

        now = time.time()
        time_passed = now - self.last_tick
        self.last_tick = now

        return time_passed

class Window:
    def __init__(self, size, title, cursor = False):
        pygame.init()
        pygame.mixer.quit()

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        pygame.mouse.set_visible(cursor)

        self.rect = self.screen.get_rect()

    @property
    def width(self): return self.rect.width
    @property
    def height(self): return self.rect.height

    # Returns whether a mouse button has been pressed or not.
    def mousedown(self): return next(
        (e.type == pygame.MOUSEBUTTONDOWN
        for e in self.events),
        False
    )

    def loop(self, instructions):
        while 1:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT: sys.exit()

            self.keys = pygame.key.get_pressed()

            instructions()

            pygame.display.flip() # update display Surface
