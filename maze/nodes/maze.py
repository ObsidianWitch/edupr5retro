import numpy
from retro.src import retro
from maze.path import asset

class Maze(retro.Sprite):
    def __init__(self):
        self.tile_size = 20
        retro.Sprite.__init__(self, retro.Image(asset('maze.png')))
        self.image.scale(self.tile_size)
        self.init_items()

    # Places items in the maze based on `self.image`. Each item is associated
    # with a color:
    #   yellow -> exits
    #   cyan   -> treasures
    #   red    -> traps
    def init_items(self):
        self.items     = retro.Group()
        self.treasures = retro.Group()
        self.traps     = retro.Group()

        def init_exit(xsq, ysq):
            self.exit = retro.Sprite.from_path(asset('exit.png'))
            self.exit.rect.move_ip(xsq, ysq)
            self.items.append(self.exit)

        def init_treasure(xsq, ysq):
            sprite = retro.Sprite.from_path(asset('treasure.png'))
            sprite.rect.move_ip(xsq, ysq)
            self.image.draw_rect(retro.BLACK, sprite.rect)
            self.items.append(sprite)
            self.treasures.append(sprite)

        def init_trap(xsq, ysq):
            sprite = retro.Sprite.from_path(asset('trap.png'))
            sprite.rect.move_ip(xsq, ysq)
            self.items.append(sprite)
            self.traps.append(sprite)

        for y in range(self.rect.height):
            for x in range(self.rect.width):
                xsq = x * self.tile_size
                ysq = y * self.tile_size
                color = self.image[xsq, ysq]
                if color == retro.YELLOW:
                    init_exit(xsq, ysq)
                elif color == retro.CYAN:
                    init_treasure(xsq, ysq)
                elif color == retro.RED:
                    init_trap(xsq, ysq)

    # Draw the maze and the items contained in it.
    def draw(self, target):
        retro.Sprite.draw(self, target)
        self.items.draw(target)
