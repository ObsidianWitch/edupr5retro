from game.collisions import Collisions

class Entity:
    def __init__(self, speed):
        self.speed  = speed
        self.nxtdir = [0, 0]
        self.curdir = [0, 0]

    @property
    def move_vec(self): return (
        self.speed * self.curdir[0],
        self.speed * self.curdir[1],
    )

    def bounding_rect(self, offset):
        r = self.rect.copy()
        r.size = (r.size[0] - offset, r.size[1] - offset)
        r.center = self.rect.center
        return r

    def collide_maze(self, maze):
        curcol = Collisions.pixel3(
            image = maze.image,
            dir   = self.curdir,
            rect  = self.rect,
            color = maze.C_WALL,
        )
        nxtcol = Collisions.pixel3(
            image = maze.image,
            dir   = self.nxtdir,
            rect  = self.rect,
            color = maze.C_WALL,
        )

        return (curcol, nxtcol)
