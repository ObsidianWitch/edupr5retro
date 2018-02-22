import pygame

from shared.sprite import Sprite
from lemmings.characters.lemmings import Lemmings
from lemmings.common import asset_path
from lemmings.bg import BG
from lemmings.ui import UI

class StateRun:
    def __init__(self, window):
        self.window = window
        self.bg = BG()

        self.ui = UI(self.window)

        self.lemmings = Lemmings(self.window, self.bg)
        self.exit = Sprite.from_path(
            asset_path("sortie.png"),
            position = (622, 252),
        )

        self.win = False

    def run(self):
        # update
        self.ui.update()
        self.lemmings.update(self.ui.selection.state)

        if pygame.sprite.spritecollide(
            self.exit,           # sprite
            self.lemmings.group, # group
            True                 # dokill
        ): self.lemmings.escaped += 1

        self.win = (self.lemmings.escaped >= 10)

        # Draw
        self.bg.clear()
        self.lemmings.draw_bg()

        self.window.screen.blit(self.bg.current, (0,0))
        self.exit.draw(self.window.screen)
        self.ui.draw()
        self.lemmings.draw_screen()
