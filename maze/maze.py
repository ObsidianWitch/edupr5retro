import pygame
import numpy

from shared.sprite import Sprite
from maze.palette import palette

class Maze:
    maze_ascii = [
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
    ]

    exit_ascii = [
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
    ]

    treasure_ascii = [
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
    ]

    trap_ascii = [
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
    ]

    def __init__(self, window):
        self.window = window

        self.square_size = 20
        self.height = len(self.maze_ascii)
        self.width  = len(self.maze_ascii[0])

        self.exit = Sprite.from_ascii_sprites(
            ascii_sprites = [self.exit_ascii],
            dictionary    = palette,
            position      = (0, 0),
        )

        self.treasure = Sprite.from_ascii_sprites(
            ascii_sprites = [self.treasure_ascii],
            dictionary    = palette,
            position      = (0, 0),
        )

        self.trap = Sprite.from_ascii_sprites(
            ascii_sprites = [self.trap_ascii],
            dictionary    = palette,
            position      = (0, 0),
        )

    def draw(self):
        for y, x in numpy.ndindex(self.height, self.width):
            code  = self.maze_ascii[y][x]
            color = palette[code]
            xsq   = x * self.square_size
            ysq   = y * self.square_size

            if code == "Y":
                self.window.screen.blit(self.exit.image, (xsq, ysq))
                continue
            elif code == "C":
                self.window.screen.blit(self.treasure.image, (xsq, ysq))
                continue
            elif code == "R":
                self.window.screen.blit(self.trap.image, (xsq, ysq))
                continue

            pygame.draw.rect(
                self.window.screen,
                color,
                [xsq, ysq, self.square_size, self.square_size]
            )
