import pygame
import pygame.surfarray as surfarray
import numpy as np

from lemmings.common  import asset_path
from lemmings.lemming import Lemming

class StateRun:
    def __init__(self, window):
        self.window = window

        self.bg = pygame.image.load(asset_path("map.png"))

        self.lemmings = []

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

    def run(self):
        time = int(pygame.time.get_ticks() / 100)

        # draw background
        self.window.screen.blit(self.bg, (0,0))

        # creation des lemmings : 1 lemming toutes les 1,5 secondes
        if (
            len(self.lemmings) < 5
            and ((time + len(self.lemmings)) % 15 == 0)
        ):
            self.lemmings.append(Lemming(self.window))

        for lemming in self.lemmings: lemming.update()

        self.draw_cursor()
        for lemming in self.lemmings: lemming.draw()
