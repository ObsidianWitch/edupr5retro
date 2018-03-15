import os
import sys
from src.constants import *
from src.window import Window
from src.events import Events
from src.image import Image

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Events()

spritesheet = Image.from_path(os.path.join(
    "examples", "data", "spritesheet.png"
))
spritesheet[0, 0] = GREEN
assert spritesheet[0, 0] == GREEN

background = Image(window.rect().size) \
           .fill(WHITE) \
           .draw_img(spritesheet, (0, 0))

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    pos = events.mouse_pos()
    if events.mouse_hold(): background[pos] = GREEN
    print(background[pos])

    window.draw_img(background, (0, 0))

    window.update()
