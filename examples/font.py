import sys
import pygame
from src.constants import *
from src.window import Window
from src.event import Event
from src.font import Font

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Event()

font = Font(size = 42)

txt1 = font.render(
    text = "Example 1",
)
txt1_rect = txt1.rect
txt1_rect.midtop = window.rect.midtop

txt2 = font.render(
    text      = "Example 2",
    antialias = True,
    color     = RED,
    bgcolor   = BLACK,
)
txt2_rect = txt2.rect
txt2_rect.center = window.rect.center

txt3 = font.render(
    text      = "Example 3",
    antialias = True,
    color     = BLUE,
    bgcolor   = GREEN,
)
txt3_rect = txt3.rect
txt3_rect.midbottom = window.rect.midbottom

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill(WHITE) \
          .draw_img(txt1, txt1_rect) \
          .draw_img(txt2, txt2_rect.topleft) \
          .draw_img(txt3, txt3_rect.topright)

    window.update()
