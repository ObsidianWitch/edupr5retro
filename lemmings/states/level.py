from retro.src import retro
from lemmings.nodes.spawner import Spawner
from lemmings.path import asset
from lemmings.ui import UI

class Level:
    def __init__(self, window, map, startp, endp):
        self.window = window
        self.bg = retro.Stage(asset(map))

        self.ui = UI(self.window)

        self.spawner = Spawner(self.window, self.bg, startp)
        self.exit = retro.Sprite.from_path(asset("sortie.png"))
        self.exit.rect.topleft = endp

    @property
    def win(self): return (self.spawner.escaped >= 10)

    @property
    def lost(self): return (
        self.spawner.generated and (len(self.spawner.group) <= 0)
    )

    def update(self):
        self.ui.update()
        self.spawner.update(self.ui.selection.state)

        if retro.Collisions.sprites(
            sprite = self.exit,
            lst    = self.spawner.group,
            kill   = True,
        ): self.spawner.escaped += 1

    def render(self):
        self.bg.clear_all()
        self.spawner.draw_bg()

        self.bg.draw(self.window)
        self.exit.draw(self.window)
        self.ui.draw()
        self.spawner.draw_screen()

class Level1(Level):
    def __init__(self, window):
        Level.__init__(
            self   = self,
            window = window,
            map    = "map1.png",
            startp = (250, 100),
            endp   = (622, 252),
        )

class Level2(Level):
    def __init__(self, window):
        Level.__init__(
            self   = self,
            window = window,
            map    = "map2.png",
            startp = (72, 14),
            endp   = (669, 66),
        )
