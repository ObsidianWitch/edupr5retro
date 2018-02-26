import pygame

from shared.background import Background
from shared.sprite import Sprite
from lemmings.nodes.lemmings import Lemmings
from lemmings.path import asset_path
from lemmings.ui import UI

class Level:
    def __init__(self, window, map, startp, endp):
        self.window = window
        self.bg = Background(asset_path(map))

        self.ui = UI(self.window)

        self.lemmings = Lemmings(self.window, self.bg, startp)
        self.exit = Sprite.from_path(
            asset_path("sortie.png"),
            position = endp,
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

        self.window.screen.blit(self.bg.current, self.bg.rect)
        self.exit.draw(self.window.screen)
        self.ui.draw()
        self.lemmings.draw_screen()
