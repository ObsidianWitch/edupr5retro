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

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Event()

spritesheet = Image.from_path(os.path.join(
    "examples", "data", "spritesheet.png"
))
spritesheet[0, 0] = GREEN
assert spritesheet[0, 0] == GREEN

background = Image(window.rect.size) \
           .fill(WHITE) \
           .draw_img(spritesheet, (0, 0))

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    pos = events.mouse_pos()
    if events.mouse_hold(): background[pos] = GREEN
    print(background[pos])

    window.draw_img(background, (0, 0))

    window.update()
