import pygame
import numpy

from maze.palette import palette

class Maze:
    maze_ascii = [
        'BBBBBBBBBB',
        'B        B',
        'B BB BBBBB',
        'B B  B   B',
        'B BB BB  B',
        'B B   BB B',
        'B  B  B  B',
        'BB BB BB B',
        'B   B    B',
        'BBBBBBBBBB',
    ]

    def __init__(self, window):
        self.window = window

        self.square_size = 40
        self.height = len(self.maze_ascii)
        self.width  = len(self.maze_ascii[0])

    def draw(self):
        for y, x in numpy.ndindex(self.height, self.width):
            c = palette[self.maze_ascii[y][x]]
            xsq = x * self.square_size
            ysq = y * self.square_size

            pygame.draw.rect(
                self.window.screen,
                c,
                [xsq, ysq, self.square_size, self.square_size]
            )
