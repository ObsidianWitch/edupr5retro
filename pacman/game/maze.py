import math
import types
import itertools
import numpy
from retro.src import retro
from pacman.game.assets import assets

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
        self.rect.topleft = numpy.add(pos, bonus.offset).tolist()
        self.id = bonus.id
        self.value = bonus.value

        return self

    def __init__(self, pos, color): pass

class Bonuses(list):
    IMG = None

    def __init__(self):
        self.count = 0
        list.__init__(self, [])
        for (i, x), (j, y) in Maze.iterator():
            if j == 0: self.append([])
            pos = (x + 6, y + 6)
            b = Bonus(pos, self.IMG[pos])
            self[i].append(b)
            if b: self.count += 1

    def copy(self):
        new = list.__new__(self.__class__)
        new.count = self.count
        list.__init__(new, [lst.copy() for lst in self])
        return new

    def iterator(self):
        for i, line in enumerate(self):
            for j, b in enumerate(line):
                yield i, j, b

    # Search inside growing neighborhoods until a bonus is found.
    def nearest(self, sprite):
        max_reach = max(len(Maze.RANGEW), len(Maze.RANGEH))

        for reach in range(0, max_reach):
            _, _, b = next(self.neighborhood(sprite, reach), (None, None, None))
            if b: return b

        return None

    # Iterator yielding bonuses contained inside a neighborhood centered around
    # `sprite` and defined by a hollow rectangle of a specific `reach`.
    # examples:
    # reach = 0 | reach = 1 | reach = 2
    # ·····     | ·····     | ▫▫▫▫▫
    # ·····     | ·▫▫▫·     | ▫···▫
    # ··▫··     | ·▫s▫·     | ▫·s·▫
    # ·····     | ·▫▫▫·     | ▫···▫
    # ·····     | ·····     | ▫▫▫▫▫
    def neighborhood(self, sprite, reach = 0):
        i, j = Maze.tile_pos(sprite.rect.center)
        if reach == 0: it = ((0, 0),)
        else: it = itertools.chain(
            itertools.product(range(-reach, reach + 1), (-reach, reach)),
            itertools.product((-reach, reach), range(-reach + 1, reach)),
        )

        for k, l in it:
            k += i ; l += j
            if not Maze.inside(k, l): continue
            b = self[k][l]
            if b: yield k, l, b

    def remove(self, i, j):
        self[i][j] = None
        self.count -= 1

    def draw(self, image):
        for _, _, b in self.iterator():
            if b: image.draw_img(b.image, b.rect)

class Walls(list):
    COLOR = (33, 33, 222)

    def __init__(self):
        list.__init__(self, [])
        for (i, x), (j, y) in Maze.iterator():
            if j == 0: self.append([])
            pos = (x + 8, y + 8)
            w = self.square3(pos)
            self[i].append(1 if w else 0)

    @classmethod
    def pxchecker(cls, image, color):
        def inside(p): return image.rect().collidepoint(p)

        def check(p, offset):
            p = numpy.add(p, offset).tolist()
            if not inside(p): return None
            return (image[p] == color)

        return check

    @classmethod
    def px3(cls, dir, rect):
        check = cls.pxchecker(Maze.IMG, cls.COLOR)
        if dir[0] == -1: return (
            check(rect.topleft,       (-1,  0))
            or check(rect.midleft,    (-1,  0))
            or check(rect.bottomleft, (-1, -1))
        )
        elif dir[0] == 1: return (
            check(rect.topright,       ( 0,  0))
            or check(rect.midright,    ( 0,  0))
            or check(rect.bottomright, ( 0, -1))
        )
        elif dir[1] == -1: return (
            check(rect.topleft,     ( 0, -1))
            or check(rect.midtop,   ( 0, -1))
            or check(rect.topright, (-1, -1))
        )
        elif dir[1] == 1: return (
            check(rect.bottomleft,     ( 0,  0))
            or check(rect.midbottom,   ( 0,  0))
            or check(rect.bottomright, (-1,  0))
        )
        else: return False

    @classmethod
    def square3(cls, center):
        check = check = cls.pxchecker(Maze.IMG, cls.COLOR)
        it = itertools.product(range(-1, 2), repeat = 2)
        return any(check(p = center, offset = (i, j)) for i, j in it)

    # returns the number of floor cells available on the left, right, top and
    # bottom of the (`i`, `j`) cell
    def floor_cells(self, i, j):
        def helper(it1, it2):
            counter = 0
            for i, j in itertools.product(it1, it2):
                if not Maze.inside(i, j): break
                if self[i][j] == 1: break
                counter += 1
            return counter

        return (
            helper(range(i - 1, -1, -1), [j]),           # left
            helper(range(i + 1, len(Maze.RANGEW)), [j]), # right
            helper([i], range(j - 1, -1, -1)),           # top
            helper([i], range(j + 1, len(Maze.RANGEH))), # bottom
        )

class Maze(retro.Sprite):
    IMG = None
    RANGEW = None
    RANGEH = None
    WALLS = None
    BONUSES = None

    # Defer constants initialization to avoid circular dependency and to be able
    # to configure them torugh `parameters`.
    def __new__(cls, name):
        if not cls.IMG:
            cls.IMG = retro.Image.from_path(
                assets(name + "_maze.png")
            )
            cls.RANGEW = range(0, cls.IMG.rect().w, 16)
            cls.RANGEH = range(0, cls.IMG.rect().h, 16)
            Bonuses.IMG = retro.Image.from_path(
                assets(name + "_bonuses.png")
            )
        if not cls.WALLS: cls.WALLS = Walls()
        if not cls.BONUSES: cls.BONUSES = Bonuses()
        return retro.Sprite.__new__(cls)

    def __init__(self, parameters):
        retro.Sprite.__init__(self, self.IMG.copy())
        self.bonuses = self.BONUSES.copy()
        self.walls = self.WALLS

    # Checks whether the (`i, `j`) coordinates are inside the maze.
    @classmethod
    def inside(cls, i, j): return (
        i in range(len(cls.RANGEW))
        and j in range(len(cls.RANGEH))
    )

    @classmethod
    def tile_pos(cls, pos):
        return (pos[0] // 16, pos[1] // 16)

    # Returns a Maze iterator.
    # If `window` is specified, iterates over the neighborhood centered on
    # `window.center` and of reach `window.reach`.
    @classmethod
    def iterator(self, transpose = False, window = None):
        def windowit(range, i):
            minv = window.center[i] - window.reach
            maxv = window.center[i] + window.reach + 1
            if minv < 0: maxv += abs(minv) ; minv = 0
            if maxv >= len(range): minv -= maxv - len(range) ; maxv = len(range)
            return itertools.islice(enumerate(range), minv, maxv)

        it1, it2 = enumerate(self.RANGEW), enumerate(self.RANGEH)
        if window: it1, it2 = windowit(self.RANGEW, 0), windowit(self.RANGEH, 1)
        if transpose: it1, it2 = it2, it1
        for ix, jy in itertools.product(it1, it2):
            if transpose: ix, jy = jy, ix
            yield ix, jy

    def draw(self, image):
        retro.Sprite.draw(self, image)
        self.bonuses.draw(image)
