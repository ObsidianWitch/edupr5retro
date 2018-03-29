import retro
from game.collisions import Collisions

class Entity(retro.AnimatedSprite):
    def __init__(self, sprite, pos, speed, curdir = [0, 0], nxtdir = [0, 0]):
        retro.AnimatedSprite.__init__(self, sprite.images, sprite.animations)
        self.rect.topleft = pos
        self.speed  = speed
        self.curdir = curdir
        self.nxtdir = nxtdir

    def set_animation(self, name):
        if   self.curdir[0] == -1: self.animations.set(f"{name}_R")
        elif self.curdir[0] ==  1: self.animations.set(f"{name}_L")
        elif self.curdir[1] == -1: self.animations.set(f"{name}_U")
        elif self.curdir[1] ==  1: self.animations.set(f"{name}_D")

    def bounding_rect(self, offset):
        r = self.rect.copy()
        r.size = (r.size[0] - offset, r.size[1] - offset)
        r.center = self.rect.center
        return r

    def mazecol(self, maze):
        def col(dir): return Collisions.px3(
            image = maze.image,
            dir   = dir,
            rect  = self.rect,
            color = maze.C_WALL,
        )
        return (col(self.curdir), col(self.nxtdir))

    def update(self, maze):
        if not self.collide_maze(maze): self.rect.move((
            self.speed * self.curdir[0],
            self.speed * self.curdir[1],
        ))
        retro.AnimatedSprite.update(self)
