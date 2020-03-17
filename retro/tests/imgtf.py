import pygame
from src.constants import *
from src.window import Window
from src.image import Image

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
obj1_rect.move_ip(10, 10)
print(obj1_rect)

obj2 = obj1.copy().colorkey(
    color = BLACK
).flip(
    x = True,
    y = False,
)
obj2_rect = obj2.rect()
obj2_rect.move_ip(100, 10)

obj3 = Image((50, 50)).fill(
    color = BLUE
).draw_rect(
    color = WHITE,
    rect  = pygame.Rect(10, 10, 25, 25),
    width = 4,
).rotate(45)
obj3_rect = obj3.rect()
obj3_rect.move_ip(10, 100)

obj4 = obj3.copy().resize((25, 25))
obj4_rect = obj4.rect()
obj4_rect.topleft = obj3_rect.topleft
obj4_rect.move_ip(0, 100)

obj5 = obj3.copy().scale(2.0)
obj5_rect = obj5.rect()
obj5_rect.topleft = obj3_rect.topleft
obj5_rect.move_ip(0, 150)

def main():
    window.fill(WHITE) \
          .draw_img(obj1, obj1_rect.topleft) \
          .draw_img(obj2, obj2_rect.topleft) \
          .draw_img(obj3, obj3_rect.topleft) \
          .draw_img(obj4, obj4_rect.topleft) \
          .draw_img(obj5, obj5_rect.topleft)

window.loop(main)
