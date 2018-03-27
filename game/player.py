import retro
from game.entity import Entity
from game.collisions import Collisions
from game.assets import assets

class Powerup:
    def __init__(self): self.timer = retro.Timer()

    @property
    def enabled(self): return not self.timer.finished

    @property
    def started(self): return self.enabled and (0 <= self.timer.elapsed <= 1)

    def start(self): self.timer = retro.Timer(end = 50, period = 100)

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
                    "STOP_L":  [0],
                    "STOP_U":  [2],
                    "STOP_R":  [4],
                    "STOP_D":  [6],
                    "WALK_L":  range(0, 2),
                    "WALK_U":  range(2, 4),
                    "WALK_R":  range(4, 6),
                    "WALK_D":  range(6, 8),
                },
                period = 50,
            ),
        )
        self.rect.topleft = (208, 264)

        Entity.__init__(self, speed = 4)

        self.score = 0
        self.bonuses = 0
        self.powerup = Powerup()

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 4)

    def collide_bonus(self, maze, bonus):
        sr = self.bounding_rect

        bonuscol = Collisions.px1(
            image = maze.image,
            dir   = self.curdir,
            rect  = sr,
            color = bonus.color,
        )
        if not bonuscol: return

        br = retro.Rect(0, 0, 0, 0)
        br.size = (
            abs(self.curdir[0]) * (sr.w // 2) + bonus.size[0],
            abs(self.curdir[1]) * (sr.h // 2) + bonus.size[1],
        )
        br.center = sr.center
        br.centerx += self.curdir[0] * (br.w // 2)
        br.centery += self.curdir[1] * (br.h // 2)
        maze.image.draw_rect(retro.BLACK, br)

        self.score += bonus.value
        self.bonuses += 1

        if (bonus == maze.BONUS2): self.powerup.start()

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
        self.collide_bonus(maze, maze.BONUS1)
        self.collide_bonus(maze, maze.BONUS2)
        self.rect.move(self.move_vec)
        retro.AnimatedSprite.update(self)

    def draw_score(self, image):
        font = retro.Font(36)
        txt = retro.Sprite(font.render(
            text    = f"SCORE: {self.score}",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        txt.rect.bottomleft = image.rect().bottomleft
        txt.draw(image)
