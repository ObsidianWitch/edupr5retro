import retro
from game.assets import assets

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL   = ( 33,  33, 222)
    C_BONUS1 = (255, 184, 151)
    C_BONUS2 = (255, 136,  84)
    N_BONUS  = 244

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())
