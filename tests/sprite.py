import os
import sys
from src.constants import *
from src.window import Window
from src.events import Events
from src.image import Image
from src.sprite import Sprite, AnimatedSprite, Animations

def assets(filename): return os.path.join("tests", "data", filename)

window = Window(
    title     = "window",
    size      = (320, 240),
    framerate = 60,
)
events = Events()

s1 = Sprite(Image.from_path(assets("img.png")))
s1_dy = 1

i2 = Image.from_spritesheet(
    path          = assets("spritesheet.png"),
    sprite_size   = (30, 30),
    discard_color = RED,
)[0]
i2 = [img.copy() for img in i2] \
     + [img.flip(x = True, y = False) for img in i2]
s2 = AnimatedSprite(
    images     = i2,
    animations = Animations(
        data = {
            "WALK_L":  range(0, 8),
            "WALK_R":  range(0 + 8, 8 + 8),
        },
        period  = 100,
    ),
)
s2.animations.set("WALK_R")
s2.rect.top = s1.rect.bottom
s2_dx = 1

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    if   s1.rect.top < 0: s1_dy = 1
    elif s1.rect.bottom >= window.rect().h: s1_dy = -1
    s1.rect.move(0, s1_dy)

    if s2.rect.left < 0:
        s2.animations.set("WALK_R")
        s2_dx = 1
    elif s2.rect.right >= window.rect().w:
        s2.animations.set("WALK_L")
        s2_dx = -1
    s2.rect.move(s2_dx, 0)
    s2.update()

    window.fill(WHITE)
    s1.draw(window)
    s2.draw(window)

    window.update()
