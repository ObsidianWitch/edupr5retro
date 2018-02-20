import pygame
import pygame.surfarray as surfarray
import numpy as np

from shared.timer import Timer
from lemmings.common  import asset_path
from lemmings.lemming import Lemming

class StateRun:
    def __init__(self, window):
        self.window = window

        self.bg = pygame.image.load(asset_path("map.png"))
        self.lemmings = []
        self.repop_timer = Timer(15, 100)

    def draw_cursor(self):
        display = next(
            (e.type == pygame.MOUSEBUTTONDOWN for e in self.window.events),
            False
        )
        if not display: return

        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        pygame.draw.line(
            self.window.screen,
            pygame.Color("white"),
            (x - 5, y), (x + 5, y)
        )
        pygame.draw.line(
            self.window.screen,
            pygame.Color("white"),
            (x, y - 5), (x, y + 5)
        )
        print(f"Click - Grid coordinates: {x}, {y}")

    # Creates one lemming every 1.5s if the limit has not been reached.
    def generate_lemmings(self):
        if (len(self.lemmings) < 5) and self.repop_timer.finished:
            self.lemmings.append(Lemming(self.window))
            self.repop_timer.restart()

    def run(self):
        # draw background
        self.window.screen.blit(self.bg, (0,0))

        self.generate_lemmings()

        for lemming in self.lemmings: lemming.update()

        self.draw_cursor()
        for lemming in self.lemmings: lemming.draw()
