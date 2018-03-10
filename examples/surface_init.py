import os
import sys
import pygame
import numpy
from src.constants import *
from src.window import Window
from src.event import Event
from src.surface import Surface

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

PALETTE = {
    ' ': (  0,   0,   0),
    'W': (255, 255, 255),
    'R': (255,   0,   0),
    'G': (  0, 255,   0),
    'B': (  0,   0, 255),
    'C': (  0, 225, 255),
    'Y': (255, 255,   0),
}

ASCII_IMG = (
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

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Event()

def from_ascii(txt, dictionary):
    height = len(txt)
    width  = len(txt[0])

    rgb_sprite = numpy.zeros((width, height, 3))
    for y, x in numpy.ndindex(height, width):
        c = txt[y][x]
        rgb_sprite[x,y] = dictionary[c]

    return Surface.from_array(rgb_sprite)

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    s1 = Surface((100, 100))
    s2 = Surface.from_image(os.path.join(
        "examples", "data", "img.png"
    ))
    s3 = from_ascii(ASCII_IMG, PALETTE)

    window.fill(color = WHITE) \
          .draw_surface(s1, (10, 10)) \
          .draw_surface(s2, (10, 110)) \
          .draw_surface(s3, (10, 170))

    print(events.mouse_pos())

    window.update()
