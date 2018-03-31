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
    COUNT = 0

    @classmethod
    def init(cls):
        itw = enumerate(range(22, cls.IMG.rect().w, 16))
        ith = enumerate(range(22, cls.IMG.rect().h, 16))

        for (i, x), (j, y) in itertools.product(itw, ith):
            if j == 0: cls.BONUSES.append([])
            b = Bonus((x, y), cls.IMG[x, y])
            cls.BONUSES[i].append(b)
            if b: cls.COUNT += 1

    def __init__(self):
        if self.COUNT == 0: self.init()
        list.__init__(self, [l.copy() for l in self.BONUSES])
        self.count = self.COUNT

    def iterator(self):
        for i, _ in enumerate(self):
            for _, b in enumerate(self[i]):
                if b: yield b

    def chunkxy(self, pos, div = 2):
        lx = self.IMG.rect().w // div
        ly = self.IMG.rect().h // div
        i = pos[0] // lx
        j = pos[1] // ly
        return self.chunk(i, j, div)

    def chunk(self, i, j, div = 2):
        def iterator(seq, k):
            l = len(seq) // div
            return itertools.islice(enumerate(seq), k * l, (k + 1) * l)

        for x,_ in iterator(self, i):
            for y, b in iterator(self[x], j):
                if b: yield x, y, b

    def remove(self, x, y):
        self[x][y] = None
        self.count -= 1

    def draw(self, image):
        for b in self.iterator():
            image.draw_img(b.image, b.rect)

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL  = (33, 33, 222)

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())
        self.bonuses = Bonuses()

    def draw(self, image):
        retro.Sprite.draw(self, image)
        self.bonuses.draw(image)
