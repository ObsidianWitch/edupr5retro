import pygame
import numpy

from shared.sprite import Sprite
from maze.nodes.palette import palette

class Maze:
    maze_ascii = (
        'BBBBBBBBBBBBBBBBBBBB',
        'B         B       CB',
        'B BB BBBBB     BBBBB',
        'BRB  B      B  BC  B',
        'BCBB BB  BB BBRBB  B',
        'B BC  BB BB B   BB B',
        'B  B  B  BB  B  B  B',
        'BB BB BB BBB BB BB B',
        'B   B    R   YB    B',
        'B   B    BBB BB BB B',
        'BB BB BB   RBB BB  B',
        'B        BB        B',
        'B B  BBBBB  BB BBBBB',
        'B B  B   BB B  BBBBB',
        'B B  BB   B  B BBBCB',
        'B B   BB    B   BB B',
        'B  B  B      B  BB B',
        'BB BB B  BBB BB BB B',
        'B  CB    BBB  B    B',
        'BBBBBBBBBBBBBBBBBBBB',
    )

    exit_ascii = (
        '                    ',
        '                    ',
        '        YYYY        ',
        '       YYYYYY       ',
        '      YYY  YYY      ',
        '      YY    YY      ',
        '      YY    YY      ',
        '      YYY  YYY      ',
        '       YYYYYY       ',
        '        YYYY        ',
        '         YY         ',
        '         YY         ',
        '         YY         ',
        '       YYYY         ',
        '       YYYY         ',
        '        YYY         ',
        '       YYYY         ',
        '         YY         ',
        '                    ',
        '                    ',
    )

    treasure_ascii = (
        '                    ',
        '                    ',
        '                    ',
        '                    ',
        '                    ',
        '    CCCCCCCCCCCC    ',
        '  CCCWWCCCCCCCCCCC  ',
        '  CCCWWCCCCCCCCCCC  ',
        '   CCCCCCCCCCCCCC   ',
        '    CCCCCCCCCCCC    ',
        '     CCCCCCCCCC     ',
        '      CCCCCCCC      ',
        '       CCCCCC       ',
        '        CCCC        ',
        '         CC         ',
        '                    ',
        '                    ',
        '                    ',
        '                    ',
        '                    ',
    )

    trap_ascii = (
        '                    ',
        '                    ',
        '          RRRR      ',
        '        RRYRRRR     ',
        '       RRYRR   R    ',
        '       RYYRRRR      ',
        '     RRRYYRYYRRR    ',
        '    RYRRYRYYYYRRR   ',
        '    RYYYYRRRYYYRR   ',
        '    RRYYRRRRYRRRR   ',
        '  R RRYRRRRRRYRR    ',
        '  R  RRYRRRRRYR     ',
        '  RRRRYYYRRRYYYR    ',
        '   RRRRYYYRYRRYR    ',
        '     RRRRRYYRRRR    ',
        '    R  RRYYRR RR    ',
        '     RRRRRRR  R     ',
        '       RRRR  R      ',
        '                    ',
        '                    ',
    )

    exit_img = Sprite.ascii_to_image(
        txt        = exit_ascii,
        dictionary = palette,
    )

    treasure_img = Sprite.ascii_to_image(
        txt        = treasure_ascii,
        dictionary = palette,
    )

    trap_img = Sprite.ascii_to_image(
        txt        = trap_ascii,
        dictionary = palette,
    )

    def __init__(self, window):
        self.window = window

        self.square_size = 20
        self.height = len(self.maze_ascii)
        self.width  = len(self.maze_ascii[0])

        self.init_items()

    # Places items in the maze based on the `maze_ascii` map.
    # Each item is associated with a code contained in `palette`.
    # "Y" -> exits
    # "C" -> treasures
    # "R" -> traps
    def init_items(self):
        self.items     = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        self.traps     = pygame.sprite.Group()

        def init_one(code, color, xsq, ysq):
            if code == "Y":
                sprite = Sprite(
                    image    = self.exit_img,
                    position = (xsq, ysq),
                )
                self.items.add(sprite)
                self.exit = sprite
            elif code == "C":
                sprite = Sprite(
                    image    = self.treasure_img,
                    position = (xsq, ysq),
                )
                self.items.add(sprite)
                self.treasures.add(sprite)
            elif code == "R":
                sprite = Sprite(
                    image    = self.trap_img,
                    position = (xsq, ysq),
                )
                self.items.add(sprite)
                self.traps.add(sprite)

        self.traverse(init_one)

    # Traverses the maze array and executes the given `function` on each
    # element.
    def traverse(self, function):
        for y, x in numpy.ndindex(self.height, self.width):
            code  = self.maze_ascii[y][x]
            color = palette[code]
            xsq   = x * self.square_size
            ysq   = y * self.square_size

            function(code, color, xsq, ysq)

    # Draw the maze and the items contained in it.
    def draw(self):
        def draw_one(code, color, xsq, ysq):
            # skip item tiles (drawing handled by sprites)
            if code in ("Y", "C", "R"): color = palette[" "]

            pygame.draw.rect(
                self.window.screen,
                color,
                [xsq, ysq, self.square_size, self.square_size]
            )

        self.traverse(draw_one)

        self.items.draw(self.window.screen)
