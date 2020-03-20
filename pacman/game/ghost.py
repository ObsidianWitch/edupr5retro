import enum
import random
import numpy
from retro.src import retro
from pacman.game.entity import Entity
from pacman.game.assets import assets

class Ghosts(retro.Group):
    def __init__(self, num, pos):
        retro.Group.__init__(self, Ghost(pos))
        self.num = num
        self.pos = pos
        self.spawn_timer = retro.Counter(end = 50, period = 100)

    def notify_kill(self):
        self.spawn_timer.restart()

    def update(self, maze, player):
        retro.Group.update(self, maze, player)

        if len(self) == self.num: return
        elif self.spawn_timer.elapsed > 50:
            self.spawn_timer.restart()
        elif self.spawn_timer.finished:
            self.append(Ghost(self.pos))
            self.spawn_timer.restart()

class State:
    WALK = 0
    FEAR = 1

    def __init__(self, ghost):
        self.ghost = ghost
        self.current = self.WALK

    def __eq__(self, v): return (self.current == v)

    def update(self, player):
        if self.current == self.WALK:
            if player.powerup.started:
                self.ghost.set_animation("FEAR")
                self.ghost.curdir = numpy.negative(self.ghost.curdir).tolist()
                self.current = self.FEAR
        elif self.current == self.FEAR:
            if not player.powerup.enabled:
                self.ghost.set_animation("WALK")
                self.current = self.WALK

class Ghost(Entity):
    IMGS = retro.Image.from_spritesheet(
        path          = assets("ghost.png"),
        sprite_size   = (32, 32),
        discard_color = retro.RED,
    )

    BONUS = 200

    def __init__(self, pos):
        Entity.__init__(self,
            sprite = retro.Sprite(
                images     = self.IMGS,
                animations = retro.Animations(
                    period = 50,
                    WALK_L = [0], WALK_U = [0],
                    WALK_R = [0], WALK_D = [0],
                    FEAR_L = [1], FEAR_U = [1],
                    FEAR_R = [1], FEAR_D = [1],
                ),
            ),
            pos   = pos,
            speed = 2,
            curdir = [0, 0],
            nxtdir = random.choice(([-1, 0], [1, 0])),
        )

        self.state = State(self)

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 12)

    def next_dir(self):
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        opdir = numpy.negative(self.curdir).tolist()
        if opdir in dirs: dirs.remove(opdir)
        self.nxtdir = random.choice(dirs)

    def collide_maze(self, maze):
        if not self.nxtcol:
            self.curdir = self.nxtdir
        elif self.curcol is None:
            self.curdir = numpy.negative(self.curdir).tolist()

        elif self.curcol:
            self.next_dir()
            return True

        return False

    def kill(self):
        for g in self.groups: g.notify_kill()
        Entity.kill(self)

    def update(self, maze, player):
        self.state.update(player)
        if (self.curdir == self.nxtdir):
            self.next_dir()
        Entity.update(self, maze)
