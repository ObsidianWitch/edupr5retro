import sys
import pygame
from src.constants import *
from src.window import Window
from src.event import Event

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

    window.fill(color = WHITE)

    window.draw_line(
        color     = GREEN,
        start_pos = (0, 0),
        end_pos   = (50,30),
        width     = 5,
    )

    window.draw_rect(
        color = BLACK,
        rect  = (75, 10, 50, 20),
        width = 2,
    )

    window.draw_rect(
        color = BLACK,
        rect  = (150, 10, 50, 20),
    )

    window.draw_circle(
        color  = BLUE,
        center = (60, 250),
        radius  = 40,
    )

    window.draw_circle(
        color  = BLUE,
        center = (200, 250),
        radius  = 40,
        width   = 4,
    )

    print(events.mouse_pos())

    window.update()
