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
    RANGEW = range(22, IMG.rect().w - 16, 16)
    RANGEH = range(22, IMG.rect().h - 16, 16)
    BONUSES = []
    COUNT = 0

    @classmethod
    def init(cls):
        itw = enumerate(cls.RANGEW)
        ith = enumerate(cls.RANGEH)
        for (i, x), (j, y) in itertools.product(itw, ith):
            if j == 0: cls.BONUSES.append([])
            b = Bonus((x, y), cls.IMG[x, y])
            cls.BONUSES[i].append(b)
            if b: cls.COUNT += 1

    def __init__(self):
        if self.COUNT == 0: self.init()
        list.__init__(self, [l.copy() for l in self.BONUSES])
        self.count = self.COUNT

    def debug(self, player, ghosts):
        for i, j, s in self.symbols(player, ghosts, transpose = True):
            if j == 0: print()
            print(s, end = '')
        print()

    # Iterator returning integers each representing an element in the maze.
    def symbols(self, player, ghosts, transpose = False):
        def veq(p1, p2): return (p1[0] == p2[0]) and (p1[1] == p2[1])

        ij_player = Maze.tile_pos(player.rect.topleft)
        ij_player = (ij_player[1], ij_player[0]) if transpose else ij_player

        for i, j, b in self.iterator(transpose):
            if veq((i, j), ij_player): yield i, j, 1
            elif b: yield i, j, 2
            else: yield i, j, 0

    def iterator(self, transpose = False):
        iterable = self if not transpose else zip(*self)
        for i, line in enumerate(iterable):
            for j, b in enumerate(line):
                yield i, j, b

    def nearest(self, pos):
        max_reach = max(len(self.RANGEW), len(self.RANGEH))

        for reach in range(0, max_reach):
            _, _, b = next(self.neighborhood(pos, reach), (None, None, None))
            if b: return b

        return None

    def neighborhood(self, pos, reach = 0):
        def inside(i, j): return (
            i in range(len(self.RANGEW))
            and j in range(len(self.RANGEH))
        )

        i, j = Maze.tile_pos(pos)
        if reach == 0: it = ((0, 0),)
        else: it = itertools.chain(
            itertools.product(range(-reach, reach + 1), (-reach, reach)),
            itertools.product((-reach, reach), range(-reach + 1, reach)),
        )

        for k, l in it:
            k += i ; l += j
            if not inside(k, l): continue
            b = self[k][l]
            if b: yield k, l, b

    def remove(self, i, j):
        self[i][j] = None
        self.count -= 1

    def draw(self, image):
        for _, _, b in self.iterator():
            if b: image.draw_img(b.image, b.rect)

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL  = (33, 33, 222)

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())
        self.bonuses = Bonuses()

    @classmethod
    def tile_pos(cls, pos): return (pos[0] // 16, pos[1] // 16)

    def draw(self, image):
        retro.Sprite.draw(self, image)
        self.bonuses.draw(image)
