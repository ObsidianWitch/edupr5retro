import sys
import math
import itertools
import pygame
from retro.src.image import Image
from retro.src.events import Events
from retro.src.font import Font
from retro.src.counter import Ticker

class Window(Image):
    def __init__(self, title, size, fps, headless = False):
        pygame.init()
        Ticker.inject(self)

        self.headless = headless
        if self.headless:
            surface = pygame.Surface(size)
        else:
            pygame.display.set_caption(title)
            surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.ftick = 0

        self.events = Events()

        self.fonts = list( Font(size) for size in range(18, 43, 6) )

    def cursor(self, cursor):
        if type(cursor) is bool:
            pygame.mouse.set_visible(cursor)
        else:
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(*cursor)

    def step(self, update, render):
        self.events.update()
        if self.events.event(pygame.QUIT):
            sys.exit()

        if update:
            update()
        if render:
            render()
            pygame.display.flip()

        self.ftick += 1
        self.clock.tick(self.fps)

    def loop(self, update, render):
        while True:
            self.step(update, render)
