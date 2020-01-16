import retro
from game.maze import Walls

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
        r.size = retro.Vec.sub(r.size, offset)
        r.center = self.rect.center
        return r

    def mazecol(self, maze):
        return (
            Walls.px3(self.curdir, self.rect),
            Walls.px3(self.nxtdir, self.rect),
        )

    def collide_maze(self, maze):
        raise NotImplementedError

    def update(self, maze):
        if not self.collide_maze(maze): self.rect.move(
            retro.Vec.mul(self.speed, self.curdir)
        )
        retro.AnimatedSprite.update(self)
