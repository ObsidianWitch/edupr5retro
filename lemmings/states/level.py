import shared.retro as retro
import shared.collisions
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
        self.exit = Sprite.from_path(asset_path("sortie.png"))
        self.exit.rect.topleft = endp

    @property
    def win(self): return (self.lemmings.escaped >= 10)

    @property
    def lost(self): return (
        self.lemmings.generated and (len(self.lemmings.group) <= 0)
    )

    def run(self):
        # update
        self.ui.update()
        self.lemmings.update(self.ui.selection.state)

        if shared.collisions.sprites(
            sprite = self.exit,
            lst    = self.lemmings.group,
            kill   = True,
        ): self.lemmings.escaped += 1

        # Draw
        self.bg.clear()
        self.lemmings.draw_bg()

        self.window.draw_img(self.bg.current, self.bg.rect)
        self.exit.draw(self.window)
        self.ui.draw()
        self.lemmings.draw_screen()
