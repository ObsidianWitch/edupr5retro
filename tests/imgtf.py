import pygame
from pr5retro.constants import *
from pr5retro.window import Window
from pr5retro.image import Image

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)

obj1 = Image((100, 100)).draw_line(
    color     = GREEN,
    start_pos = (0, 0),
    end_pos   = (50,30),
    width     = 5,
)
obj1_rect = obj1.rect()
obj1_rect.move(10, 10)
print(obj1_rect)

obj2 = obj1.copy().colorkey(
    color = BLACK
).flip(
    x = True,
    y = False,
)
obj2_rect = obj2.rect()
obj2_rect.move(100, 10)
print(obj2_rect)

obj3 = Image((50, 50)).fill(
    color = BLUE
).draw_rect(
    color = WHITE,
    rect  = pygame.Rect(10, 10, 25, 25),
    width = 4,
).rotate(45)
obj3_rect = obj3.rect()
obj3_rect.move(10, 100)
print(obj3_rect)

obj4 = obj3.copy().resize((25, 25))
obj4_rect = obj4.rect()
obj4_rect.topleft = obj3_rect.topleft
obj4_rect.move(0, 100)
print(obj4_rect)

obj5 = obj3.copy().scale(2.0)
obj5_rect = obj5.rect()
obj5_rect.topleft = obj3_rect.topleft
obj5_rect.move(0, 150)
print(obj5_rect)

def main():
    window.fill(WHITE) \
          .draw_img(obj1, obj1_rect) \
          .draw_img(obj2, obj2_rect) \
          .draw_img(obj3, obj3_rect) \
          .draw_img(obj4, obj4_rect) \
          .draw_img(obj5, obj5_rect)

    print(window.events.mouse_pos())

window.loop(main)
