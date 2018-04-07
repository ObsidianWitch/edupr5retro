import enum
import random
import retro
from game.entity import Entity
from game.assets import assets

class Ghosts(retro.Group):
    def __init__(self):
        retro.Group.__init__(self, Ghost())
        self.spawn_timer = retro.Timer(end = 50, period = 100)

    def update(self, maze, player):
        retro.Group.update(self, maze, player)

        if len(self) == 4: return
        elif self.spawn_timer.elapsed > 50:
            self.spawn_timer.restart()
        elif self.spawn_timer.finished:
            self.append(Ghost())
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
                self.ghost.curdir = [
                    -self.ghost.curdir[0],
                    -self.ghost.curdir[1]
                ]
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
    )[0]

    BONUS = 200

    def __init__(self):
        Entity.__init__(self,
            sprite = retro.AnimatedSprite(
                images     = self.IMGS,
                animations = retro.Animations(
                    data = {
                        "WALK_L": [0], "WALK_U": [0],
                        "WALK_R": [0], "WALK_D": [0],
                        "FEAR_L": [1], "FEAR_U": [1],
                        "FEAR_R": [1], "FEAR_D": [1],
                    },
                    period = 50,
                ),
            ),
            pos   = (208, 168),
            speed = 2,
            curdir = [0, 0],
            nxtdir = random.choice(([-1, 0], [1, 0])),
        )

        self.state = State(self)

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 12)

    def next_dir(self):
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        opdir = [-self.curdir[0], -self.curdir[1]]
        if opdir in dirs: dirs.remove(opdir)
        self.nxtdir = random.choice(dirs)

    def collide_maze(self, maze):
        curcol, nxtcol = self.mazecol(maze)

        if not nxtcol:
            self.curdir = self.nxtdir
        elif curcol is None:
            self.curdir = [-self.curdir[0], -self.curdir[1]]
        elif curcol:
            self.next_dir()
            return True

        return False

    def update(self, maze, player):
        self.state.update(player)
        if (self.curdir == self.nxtdir): self.next_dir()
        Entity.update(self, maze)
