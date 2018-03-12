import os
import sys
import pygame
import numpy
from src.constants import *
from src.window import Window
from src.event import Event
from src.image import Image

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
s1_rect = s1.rect
s1_rect.move(10, 10)
s2 = spritesheet.subimage((30, 0, 30, 30))
s2_rect = s2.rect
s2_rect.move(50, 10)
s3 = spritesheet.subimage((0, 30, 30, 30))
s3_rect = s3.rect
s3_rect.move(10, 50)

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill(WHITE) \
          .draw_img(s1, s1_rect) \
          .draw_img(s2, s2_rect) \
          .draw_img(s3, s3_rect)

    print(events.mouse_pos())

    window.update()
