import os
import sys
import pygame
from src.constants import *
from src.window import Window
from src.event import Event
from src.surface import Surface

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

window = Window(
    title     = "events",
    size      = (640, 480),
    framerate = 30,
)
events = Event()

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    s1 = Surface((100, 100))
    s2 = Surface.from_image(os.path.join(
        "examples", "data", "img.png"
    ))

    window.fill(color = WHITE) \
          .draw_surface(s1, (10, 10)) \
          .draw_surface(s2, (10, 110))

    print(events.mouse_pos())

    window.update()
