import os
import sys
import pygame
import numpy
from src.constants import *
from src.window import Window
from src.event import Event
from src.image import Image

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

    return Image.from_array(rgb_sprite)

s1 = Image((100, 100))
s1.rect.move(10, 10)
s2 = Image.from_path(os.path.join(
    "examples", "data", "img.png"
))
s2.rect.move(10, 110)
s2_area = pygame.Rect(20, 10, 30, 30)
s3 = from_ascii(ASCII_IMG, PALETTE)
s3.rect.move(10, 150)

s4 = s3.deepcopy()
s4.rect.move(50, 0)
s5 = s4.copy()
s5.rect.move(50, 0)
s5.draw_line(GREEN, (0, 0), (30, 30))

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill(color = WHITE) \
          .draw_image(s1) \
          .draw_image(s2, s2_area) \
          .draw_image(s3) \
          .draw_image(s4) \
          .draw_image(s5)

    print(events.mouse_pos())

    window.update()
