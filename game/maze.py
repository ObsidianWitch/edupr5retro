import types
import itertools
import retro
from game.assets import assets

class Bonus(retro.Sprite):
    BONUS1 = types.SimpleNamespace(
        id     = 0,
        img    = retro.Image.from_path(assets("bonus1.png")),
        color  = (255, 184, 151),
        value  = 10,
        offset = (0, 0),
    )
    BONUS2 = types.SimpleNamespace(
        id     = 1,
        img    = retro.Image.from_path(assets("bonus2.png")),
        color  = (255, 136, 84),
        value  = 50,
        offset = (-6, -6),
    )

    def __new__(cls, pos, color):
        if   color == cls.BONUS1.color: bonus = cls.BONUS1
        elif color == cls.BONUS2.color: bonus = cls.BONUS2
        else: return None

        self = retro.Sprite.__new__(cls)
        retro.Sprite.__init__(self, bonus.img)
        self.rect.topleft = (
            pos[0] + bonus.offset[0],
            pos[1] + bonus.offset[1],
        )
        self.id = bonus.id
        self.value = bonus.value

        return self

    def __init__(self, pos, color): pass

class Bonuses(list):
    IMG = retro.Image.from_path(assets("bonuses.png"))
    BONUSES = []

    def __init__(self):
        if not self.BONUSES:
            rw = range(22, self.IMG.rect().w, 16)
            rh = range(22, self.IMG.rect().h, 16)
            for x, y in itertools.product(rw, rh):
                b = Bonus((x, y), self.IMG[x, y])
                if b: self.BONUSES.append(b)

        list.__init__(self, self.BONUSES)

    def draw(self, image):
        for s in self:
            image.draw_img(s.image, s.rect)

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL  = (33, 33, 222)

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())
        self.bonuses = Bonuses()

    def draw(self, image):
        retro.Sprite.draw(self, image)
        self.bonuses.draw(image)
