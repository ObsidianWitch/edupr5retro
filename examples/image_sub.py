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

s1 = spritesheet.subimage((0, 0, 30, 30))
s1.rect.move(10, 10)
s2 = spritesheet.subimage((30, 0, 30, 30))
s2.rect.move(50, 10)
s3 = spritesheet.subimage((0, 30, 30, 30))
s3.rect.move(10, 50)

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill(color = WHITE) \
          .draw_image(s1) \
          .draw_image(s2) \
          .draw_image(s3)

    print(events.mouse_pos())

    window.update()
