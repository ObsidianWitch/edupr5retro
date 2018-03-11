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
txt1.rect.midtop = window.rect.midtop
txt2 = font.render(
    text      = "Example 2",
    antialias = True,
    color     = (255, 0, 0),
    bgcolor   = (0, 0, 0),
)
txt2.rect.center = window.rect.center
txt3 = font.render(
    text      = "Example 3",
    antialias = True,
    color     = (0, 0, 255),
    bgcolor   = (0, 255, 0),
)
txt3.rect.midbottom = window.rect.midbottom


while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill((255, 255, 255)) \
          .draw_image(txt1) \
          .draw_image(txt2) \
          .draw_image(txt3)

    window.update()
