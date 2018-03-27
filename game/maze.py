import types
import retro
from game.assets import assets

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL  = (33, 33, 222)
    N_BONUS = 244
    BONUS1 = types.SimpleNamespace(
        value = 10,
        color = (255, 184, 151),
        size  = (4, 4),
    )
    BONUS2 = types.SimpleNamespace(
        value = 50,
        color = (255, 136, 84),
        size  = (16, 16),
    )

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())
