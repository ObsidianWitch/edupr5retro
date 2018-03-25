import os
import types
import retro

def assets(filename): return os.path.join("assets", filename)

class Collisions:
    @classmethod
    def pixels(cls, image, dir, rect, color):
        def inside(p): return image.rect().collidepoint(p)

        def check(p, offset):
            p = (p[0] + offset[0], p[1] + offset[1])
            if not inside(p): return None
            return (image[p] == color)

        # TODO simplify
        if dir == [-1, 0]: return (
            check(rect.topleft,       (-1,  0))
            or check(rect.midleft,    (-1,  0))
            or check(rect.bottomleft, (-1, -1))
        )
        elif dir == [1, 0]: return (
            check(rect.topright,       ( 0,  0))
            or check(rect.midright,    ( 0,  0))
            or check(rect.bottomright, ( 0, -1))
        )
        elif dir == [0, -1]: return (
            check(rect.topleft,     ( 0, -1))
            or check(rect.midtop,   ( 0, -1))
            or check(rect.topright, (-1, -1))
        )
        elif dir == [0, 1]: return (
            check(rect.bottomleft,      ( 0,  0))
             or check(rect.midbottom,   ( 0,  0))
             or check(rect.bottomright, (-1,  0))
        )
        else: return False

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    C_WALL = (33, 33, 222)
    def __init__(self, window):
        retro.Sprite.__init__(self, self.IMG)

class Player(retro.Sprite):
    IMG = retro.Image.from_path(assets("pacman.png"))

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG)
        self.rect.move(208, 264)
        self.nxtdir = [0, 0]
        self.curdir = [0, 0]

    def collide(self, maze):
        curcol = Collisions.pixels(
            image = maze.image,
            dir   = self.curdir,
            rect  = self.rect,
            color = Maze.C_WALL,
        )
        nxtcol = Collisions.pixels(
            image = maze.image,
            dir   = self.nxtdir,
            rect  = self.rect,
            color = Maze.C_WALL,
        )

        if curcol is None:
            if self.curdir[0]: self.rect.centerx = abs(
                self.rect.centerx - maze.rect.w
            )
            if self.curdir[1]: self.rect.centery = abs(
                self.rect.centery - maze.rect.h
            )
        if curcol: self.curdir = [0, 0]
        if not nxtcol: self.curdir = self.nxtdir


    def update(self):
        self.rect.move(self.curdir)

class Game:
    def __init__(self, window):
        self.window = window
        self.maze = Maze(window)
        self.player = Player()

    def run(self):
        # Update
        self.player.collide(self.maze)
        self.player.update()

        # Draw
        self.maze.draw(self.window)
        self.player.draw(self.window)
