import sys
import pygame
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

obj1 = Image((100, 100)).draw_line(
    color     = GREEN,
    start_pos = (0, 0),
    end_pos   = (50,30),
    width     = 5,
)
obj1.rect.move_ip(10, 10)
print(obj1.rect)

obj2 = obj1.copy().colorkey(
    color = BLACK
).flip(
    x = True,
    y = False,
)
obj2.rect.move_ip(100, 10)
print(obj2.rect)

obj3 = Image((50, 50)).fill(
    color = BLUE
).draw_rect(
    color = WHITE,
    rect  = pygame.Rect(10, 10, 25, 25),
    width = 4,
).rotate(45)
obj3.rect.move_ip(10, 100)
print(obj3.rect)

obj4 = obj3.copy().resize((25, 25))
obj4.rect.move_ip(10, 200)
print(obj4.rect)

obj5 = obj3.copy().scale(2.0)
obj5.rect.move_ip(10, 250)
print(obj5.rect)

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill(color = WHITE) \
          .draw_image(obj1) \
          .draw_image(obj2) \
          .draw_image(obj3) \
          .draw_image(obj4) \
          .draw_image(obj5)

    print(events.mouse_pos())

    window.update()
