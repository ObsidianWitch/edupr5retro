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

    obj1 = Surface((100, 100)).draw_line(
        color     = GREEN,
        start_pos = (0, 0),
        end_pos   = (50,30),
        width     = 5,
    )

    obj2 = obj1.copy().colorkey(
        color = BLACK
    ).flip(
        x = True,
        y = False,
    )

    obj3 = Surface((50, 50)).fill(
        color = BLUE
    ).draw_rect(
        color = WHITE,
        rect  = pygame.Rect(10, 10, 25, 25),
        width = 4,
    ).rotate(45)

    obj4 = obj3.copy().resize((25, 25))

    obj5 = obj3.copy().scale(2.0)

    window.fill(color = WHITE) \
          .draw_surface(obj1, (10, 10)) \
          .draw_surface(obj2, (100, 10)) \
          .draw_surface(obj3, (10, 100)) \
          .draw_surface(obj4, (10, 200)) \
          .draw_surface(obj5, (10, 250))

    print(events.mouse_pos())

    window.update()
