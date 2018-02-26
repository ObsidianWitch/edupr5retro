import pygame
import numpy

from shared.sprite import Sprite
from maze.nodes.palette import PALETTE

class Maze:
    MAZE_ASCII = (
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

    EXIT_ASCII = (
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

    TREASURE_ASCII = (
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

    TRAP_ASCII = (
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

    def __init__(self, window):
        self.window = window

        self.square_size = 20
        self.height = len(self.MAZE_ASCII)
        self.width  = len(self.MAZE_ASCII[0])

        self.init_items()

    # Places items in the maze based on the `MAZE_ASCII` map.
    # Each item is associated with a code contained in `PALETTE`.
    # "Y" -> exits
    # "C" -> treasures
    # "R" -> traps
    def init_items(self):
        self.items     = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        self.traps     = pygame.sprite.Group()

        def init_exit(code, color, xsq, ysq):
            self.exit = Sprite.from_ascii(
                txt        = self.EXIT_ASCII,
                dictionary = PALETTE,
                position   = (xsq, ysq),
            )
            self.items.add(self.exit)

        def init_treasure(code, color, xsq, ysq):
            sprite = Sprite.from_ascii(
                txt        = self.TREASURE_ASCII,
                dictionary = PALETTE,
                position   = (xsq, ysq),
            )
            self.items.add(sprite)
            self.treasures.add(sprite)

        def init_trap(code, color, xsq, ysq):
            sprite = Sprite.from_ascii(
                txt        = self.TRAP_ASCII,
                dictionary = PALETTE,
                position   = (xsq, ysq),
            )
            self.items.add(sprite)
            self.traps.add(sprite)

        def init_one(code, color, xsq, ysq):
            if   code == "Y": init_exit(code, color, xsq, ysq)
            elif code == "C": init_treasure(code, color, xsq, ysq)
            elif code == "R": init_trap(code, color, xsq, ysq)

        self.traverse(init_one)

    # Traverses the maze array and executes the given `function` on each
    # element.
    def traverse(self, function):
        for y, x in numpy.ndindex(self.height, self.width):
            code  = self.MAZE_ASCII[y][x]
            color = PALETTE[code]
            xsq   = x * self.square_size
            ysq   = y * self.square_size

            function(code, color, xsq, ysq)

    # Draw the maze and the items contained in it.
    def draw(self):
        def draw_one(code, color, xsq, ysq):
            # skip item tiles (drawing handled by sprites)
            if code in ("Y", "C", "R"): color = PALETTE[" "]

            pygame.draw.rect(
                self.window.screen,
                color,
                (xsq, ysq, self.square_size, self.square_size)
            )

        self.traverse(draw_one)

        self.items.draw(self.window.screen)
