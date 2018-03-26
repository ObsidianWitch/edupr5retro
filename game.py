import os
import types
import random
import retro

def assets(filename): return os.path.join("assets", filename)

class Collisions:
    @classmethod
    def pixel_checker(cls, image, color):
        def inside(p): return image.rect().collidepoint(p)

        def check(p, offset):
            p = (p[0] + offset[0], p[1] + offset[1])
            if not inside(p): return None
            return (image[p] == color)

        return check

    @classmethod
    def pixel1(cls, image, dir, rect, color):
        check = cls.pixel_checker(image, color)
        if   dir[0] == -1: return check(rect.midleft,   (-1,  0))
        elif dir[0] ==  1: return check(rect.midright,  ( 0,  0))
        elif dir[1] == -1: return check(rect.midtop,    ( 0, -1))
        elif dir[1] ==  1: return check(rect.midbottom, ( 0,  0))

    @classmethod
    def pixel3(cls, image, dir, rect, color):
        check = cls.pixel_checker(image, color)
        if dir[0] == -1: return (
            check(rect.topleft,       (-1,  0))
            or check(rect.midleft,    (-1,  0))
            or check(rect.bottomleft, (-1, -1))
        )
        elif dir[0] == 1: return (
            check(rect.topright,       ( 0,  0))
            or check(rect.midright,    ( 0,  0))
            or check(rect.bottomright, ( 0, -1))
        )
        elif dir[1] == -1: return (
            check(rect.topleft,     ( 0, -1))
            or check(rect.midtop,   ( 0, -1))
            or check(rect.topright, (-1, -1))
        )
        elif dir[1] == 1: return (
            check(rect.bottomleft,     ( 0,  0))
            or check(rect.midbottom,   ( 0,  0))
            or check(rect.bottomright, (-1,  0))
        )
        else: return False

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL   = ( 33,  33, 222)
    C_BONUS1 = (255, 184, 151)
    C_BONUS2 = (255, 136,  84)
    N_BONUS  = 244

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())

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
            color = Maze.C_WALL,
        )
        nxtcol = Collisions.pixel3(
            image = maze.image,
            dir   = self.nxtdir,
            rect  = self.rect,
            color = Maze.C_WALL,
        )

        return (curcol, nxtcol)

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
            color = Maze.C_BONUS1,
            size  = (4, 4),
            score = 10,
        )
        self.collide_bonus(
            maze  = maze,
            color = Maze.C_BONUS2,
            size  = (16, 16),
            score = 50,
        )
        self.rect.move(self.move_vec)
        retro.AnimatedSprite.update(self)

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

class Game:
    def __init__(self, window):
        self.window = window
        self.maze = Maze()
        self.player = Player()
        self.ghosts = Ghosts()

    @property
    def finished(self): return self.player.bonuses == Maze.N_BONUS

    def run(self):
        # Update
        self.player.update(self.maze)
        self.ghosts.update(self.player, self.maze)

        if self.ghosts.collide(self.player): self.reset()

        # Draw
        self.maze.draw(self.window)
        self.ghosts.draw(self.window)
        self.player.draw(self.window)

    def reset(self): self.__init__(self.window)
