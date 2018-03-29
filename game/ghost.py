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

class Ghost(Entity):
    STATES = enum.Enum("STATES", "WALK FEAR")

    DIRS = ([-1, 0], [1, 0], [0, -1], [0, 1])

    BONUS = 200

    IMGS = retro.Image.from_spritesheet(
        path          = assets("ghost.png"),
        sprite_size   = (32, 32),
        discard_color = retro.RED,
    )[0]

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
            curdir = random.choice(([-1, 0], [1, 0])),
            nxtdir = random.choice(self.DIRS),
        )

        self.state = self.STATES.WALK

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 12)

    def next_dir(self):
        choice = list(self.DIRS)
        opdir = [-self.curdir[0], -self.curdir[1]]
        if opdir in choice: choice.remove(opdir)
        self.nxtdir = random.choice(choice)

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
        if self.state == self.STATES.WALK:
            if player.powerup.started:
                self.set_animation("FEAR")
                self.curdir = [-self.curdir[0], -self.curdir[1]]
                self.state = self.STATES.FEAR
        elif self.state == self.STATES.FEAR:
            if not player.powerup.enabled:
                self.set_animation("WALK")
                self.state = self.STATES.WALK

        if (self.curdir == self.nxtdir): self.next_dir()
        Entity.update(self, maze)
