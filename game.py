import os
import types
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
    def pixel_vertices(cls, image, rect, color):
        check = cls.pixel_checker(image, color)

        return types.SimpleNamespace(
            up    = check(rect.topleft,     ( 0, -1))
                 or check(rect.topright,    (-1, -1)),
            down  = check(rect.bottomleft,  ( 0,  0))
                 or check(rect.bottomright, (-1,  0)),
            left  = check(rect.topleft,     (-1,  0))
                 or check(rect.bottomleft,  (-1, -1)),
            right = check(rect.topright,    ( 0,  0))
                 or check(rect.bottomright, ( 0, -1)),
        )

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
        self.speed = [0, 0]

    def collide(self, maze):
        collisions = Collisions.pixel_vertices(
            image = maze.image,
            rect  = self.rect,
            color = Maze.C_WALL,
        )

        if   collisions.up    is None: self.rect.bottom = maze.rect.bottom
        elif collisions.down  is None: self.rect.top    = maze.rect.top
        elif collisions.left  is None: self.rect.right  = maze.rect.right
        elif collisions.right is None: self.rect.left   = maze.rect.left

        if collisions.up    and (self.speed[1] == -1): self.speed[1] = 0
        if collisions.down  and (self.speed[1] ==  1): self.speed[1] = 0
        if collisions.left  and (self.speed[0] == -1): self.speed[0] = 0
        if collisions.right and (self.speed[0] ==  1): self.speed[0] = 0

    def update(self):
        self.rect.move(self.speed)

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
        self.window.fill(retro.BLACK)
        self.maze.draw(self.window)
        self.player.draw(self.window)
