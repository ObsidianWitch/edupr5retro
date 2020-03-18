import numpy
import shared.retro as retro
from maze.nodes.palette import *

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

        self.tile_size = 20
        self.init_items()
        self.init_maze()

    # Places items in the maze based on the `MAZE_ASCII` map.
    # Each item is associated with a code contained in `PALETTE`.
    # "Y" -> exits
    # "C" -> treasures
    # "R" -> traps
    def init_items(self):
        self.items     = retro.Group()
        self.treasures = retro.Group()
        self.traps     = retro.Group()

        def init_exit(code, color, xsq, ysq):
            self.exit = retro.Sprite.from_ascii(
                txt        = self.EXIT_ASCII,
                dictionary = SPRITE_PALETTE,
            )
            self.exit.rect.move_ip(xsq, ysq)
            self.items.append(self.exit)

        def init_treasure(code, color, xsq, ysq):
            sprite = retro.Sprite.from_ascii(
                txt        = self.TREASURE_ASCII,
                dictionary = SPRITE_PALETTE,
            )
            sprite.rect.move_ip(xsq, ysq)
            self.items.append(sprite)
            self.treasures.append(sprite)

        def init_trap(code, color, xsq, ysq):
            sprite = retro.Sprite.from_ascii(
                txt        = self.TRAP_ASCII,
                dictionary = SPRITE_PALETTE,
            )
            sprite.rect.move_ip(xsq, ysq)
            self.items.append(sprite)
            self.traps.append(sprite)

        def init_one(code, color, xsq, ysq):
            if   code == "Y": init_exit(code, color, xsq, ysq)
            elif code == "C": init_treasure(code, color, xsq, ysq)
            elif code == "R": init_trap(code, color, xsq, ysq)

        self.traverse(init_one)

    def init_maze(self):
        self.maze = retro.Sprite.from_ascii(self.MAZE_ASCII, MAZE_PALETTE)
        self.maze.scale(self.tile_size)

    # Traverses the MAZE_ASCII array and executes the given `function` on each
    # element.
    def traverse(self, function):
        height = len(self.MAZE_ASCII)
        width  = len(self.MAZE_ASCII[0])

        for y, x in numpy.ndindex(height, width):
            code  = self.MAZE_ASCII[y][x]
            color = MAZE_PALETTE[code]
            xsq   = x * self.tile_size
            ysq   = y * self.tile_size

            function(code, color, xsq, ysq)

    # Draw the maze and the items contained in it.
    def draw(self):
        self.maze.draw(self.window)
        self.items.draw(self.window)
