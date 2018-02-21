import pygame

from lemmings.common  import asset_path
from lemmings.lemmings import Lemmings
from lemmings.ui import UI

class StateRun:
    def __init__(self, window):
        self.window = window
        self.bg = pygame.image.load(asset_path("map.png"))
        self.lemmings = Lemmings(self.window, self.bg)
        self.ui = UI(self.window)

    def run(self):
        # update
        self.ui.update()
        self.lemmings.update()

        # Draw
        self.window.screen.blit(self.bg, (0,0))
        self.ui.draw()
        self.lemmings.draw()
