import sys
import pygame

class Window:
    @property
    def width(self): return self.rect.width
    @property
    def height(self): return self.rect.height

    def __init__(self, size, title, cursor = False):
        pygame.init()

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        pygame.mouse.set_visible(cursor)

        self.rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()

        # Ascending size fonts
        self.fonts = list(
            pygame.font.SysFont(None, size)
            for size in range(18, 43, 6)
        )

    # Returns whether a mouse button has been pressed or not.
    def mousedown(self): return next(
        (e.type == pygame.MOUSEBUTTONDOWN
        for e in self.events),
        False
    )

    # Returns whether `key` has been pressed or not by checking the
    # `events` list. To check if `key` is held down, use the `self.keys` list
    # instead.
    def keydown(self, key): return next(
        (e.type == pygame.KEYDOWN and e.key == key
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

            self.clock.tick(30) # 30 FPS
            pygame.display.flip() # update display Surface
