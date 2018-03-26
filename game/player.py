import retro
from game.entity import Entity
from game.collisions import Collisions
from game.assets import assets

class Player(retro.AnimatedSprite, Entity):
    IMGS = retro.Image.from_spritesheet(
        path          = assets("pacman.png"),
        sprite_size   = (32, 32),
        discard_color = retro.RED,
    )[0]
    IMGS = [img.copy() for img in IMGS] \
         + [img.copy().rotate(90) for img in IMGS] \
         + [img.copy().rotate(180) for img in IMGS] \
         + [img.copy().rotate(270) for img in IMGS]

    def __init__(self):
        retro.AnimatedSprite.__init__(
            self = self,
            images = self.IMGS,
            animations = retro.Animations(
                data = {
                    "DEFAULT": [0],
                    "WALK_L":  range(0, 2),
                    "STOP_L":  [0],
                    "WALK_U":  range(2, 4),
                    "STOP_U":  [2],
                    "WALK_R":  range(4, 6),
                    "STOP_R":  [4],
                    "WALK_D":  range(6, 8),
                    "STOP_D":  [6],
                },
                period = 50,
            ),
        )
        self.rect.topleft = (208, 264)
        Entity.__init__(self, speed = 4)
        self.score = 0
        self.bonuses = 0

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 4)

    def collide_bonus(self, maze, color, size, score):
        sr = self.bounding_rect

        bonuscol = Collisions.pixel1(
            image = maze.image,
            dir   = self.curdir,
            rect  = sr,
            color = color,
        )
        if not bonuscol: return

        br = retro.Rect(0, 0, 0, 0)
        br.size = (
            abs(self.curdir[0]) * (sr.w // 2) + size[0],
            abs(self.curdir[1]) * (sr.h // 2) + size[1],
        )
        br.center = sr.center
        br.centerx += self.curdir[0] * (br.w // 2)
        br.centery += self.curdir[1] * (br.h // 2)
        maze.image.draw_rect(retro.BLACK, br)

        self.score += score
        self.bonuses += 1

    def collide_maze(self, maze):
        curcol, nxtcol = Entity.collide_maze(self, maze)

        if curcol is None:
            if self.curdir[0]: self.rect.centerx = abs(
                self.rect.centerx - maze.rect.w
            )
            if self.curdir[1]: self.rect.centery = abs(
                self.rect.centery - maze.rect.h
            )
        elif not nxtcol:
            self.set_animation("WALK")
            self.curdir = self.nxtdir
        elif curcol:
            self.set_animation("STOP")
            self.curdir = [0, 0]


    def set_animation(self, name):
        if   self.curdir[0] == -1: self.animations.set(f"{name}_R")
        elif self.curdir[0] ==  1: self.animations.set(f"{name}_L")
        elif self.curdir[1] == -1: self.animations.set(f"{name}_U")
        elif self.curdir[1] ==  1: self.animations.set(f"{name}_D")

    def update(self, maze):
        self.collide_maze(maze)
        self.collide_bonus(
            maze  = maze,
            color = maze.C_BONUS1,
            size  = (4, 4),
            score = 10,
        )
        self.collide_bonus(
            maze  = maze,
            color = maze.C_BONUS2,
            size  = (16, 16),
            score = 50,
        )
        self.rect.move(self.move_vec)
        retro.AnimatedSprite.update(self)
