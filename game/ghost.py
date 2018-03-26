import random
import retro
from game.entity import Entity
from game.assets import assets

class Ghosts(retro.Group):
    def __init__(self):
        retro.Group.__init__(self, Ghost())
        self.spawn_timer = retro.Timer(end = 50, period = 100)

    def collide(self, player):
        for ghost in self:
            if player.bounding_rect.colliderect(ghost.bounding_rect):
                return True
        return False

    def update(self, player, *args):
        retro.Group.update(self, *args)
        if len(self) == 4: return
        elif self.spawn_timer.elapsed > 50:
            self.spawn_timer.restart()
        elif self.spawn_timer.finished:
            self.append(Ghost())
            self.spawn_timer.restart()

class Ghost(retro.Sprite, Entity):
    IMGS = retro.Image.from_spritesheet(
        path          = assets("ghost.png"),
        sprite_size   = (32, 32),
        discard_color = retro.RED,
    )[0]
    IMG_WALK = IMGS[0]
    IMG_FEAR = IMGS[1]
    DIRS = ([-1, 0], [1, 0], [0, -1], [0, 1])

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG_WALK)
        self.rect.topleft = (208, 168)

        Entity.__init__(self, speed = 2)
        self.curdir = random.choice(([-1, 0], [1, 0]))
        self.nxtdir = random.choice(self.DIRS)

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 12)

    def next_dir(self):
        choice = list(self.DIRS)
        opdir = [-self.curdir[0], -self.curdir[1]]
        if opdir in choice: choice.remove(opdir)
        self.nxtdir = random.choice(choice)

    def collide_maze(self, maze):
        curcol, nxtcol = Entity.collide_maze(self, maze)
        if not nxtcol:
            self.curdir = self.nxtdir
        elif curcol is None:
            self.curdir = [-self.curdir[0], -self.curdir[1]]
        elif curcol:
            self.next_dir()
            return True

        return False

    def update(self, maze):
        if (self.curdir == self.nxtdir): self.next_dir()
        if not self.collide_maze(maze): self.rect.move(self.move_vec)
