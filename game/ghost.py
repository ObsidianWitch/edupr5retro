import enum
import random
import retro
from game.entity import Entity
from game.assets import assets

class Ghosts(retro.Group):
    def __init__(self):
        retro.Group.__init__(self, Ghost())
        self.spawn_timer = retro.Timer(end = 50, period = 100)
        self.reset_bonus()

    # Returns 0 if no collision happened,
    #         1 if the player killed a ghost,
    #        -1 if a ghost killed the player.
    def collide(self, player):
        cghosts = [ g for g in self if g.bounding_rect.colliderect(
            player.bounding_rect
        )]
        if not cghosts: return 0

        for g in cghosts:
            if g.state != g.STATES.FEAR: return -1
            g.kill()
            player.score += self.bonus
            self.bonus *= 2

        return 1

    def reset_bonus(self): self.bonus = 200

    def update(self, maze, player):
        retro.Group.update(self, maze, player)

        if len(self) == 4: return
        elif self.spawn_timer.elapsed > 50:
            self.spawn_timer.restart()
        elif self.spawn_timer.finished:
            self.append(Ghost())
            self.spawn_timer.restart()

        if player.powerup.started: self.reset_bonus()

class Ghost(retro.Sprite, Entity):
    STATES = enum.Enum("STATES", "WALK FEAR")

    DIRS = ([-1, 0], [1, 0], [0, -1], [0, 1])

    IMGS = retro.Image.from_spritesheet(
        path          = assets("ghost.png"),
        sprite_size   = (32, 32),
        discard_color = retro.RED,
    )[0]
    IMG_WALK = IMGS[0]
    IMG_FEAR = IMGS[1]

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG_WALK)
        self.rect.topleft = (208, 168)

        Entity.__init__(self,
            speed  = 2,
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
        curcol, nxtcol = Entity.collide_maze(self, maze)
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
                self.image = self.IMG_FEAR
                self.curdir = [-self.curdir[0], -self.curdir[1]]
                self.state = self.STATES.FEAR
        elif self.state == self.STATES.FEAR:
            if not player.powerup.enabled:
                self.image = self.IMG_WALK
                self.state = self.STATES.WALK

        if (self.curdir == self.nxtdir): self.next_dir()
        if not self.collide_maze(maze): self.rect.move(self.move_vec)
