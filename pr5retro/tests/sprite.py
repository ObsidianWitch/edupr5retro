import os
from pr5retro.tests.path import assets
from pr5retro.constants import *
from pr5retro.window import Window
from pr5retro.image import Image
from pr5retro.sprite import Sprite, AnimatedSprite, Animations

window = Window(
    title     = "window",
    size      = (320, 240),
    framerate = 60,
)

s1 = Sprite(Image.from_path(assets("img.png")))
s1.dy = 1

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
s2.dx = 1

def main():
    if   s1.rect.top < 0: s1.dy = 1
    elif s1.rect.bottom >= window.rect().h: s1.dy = -1
    s1.rect.move(0, s1.dy)

    if s2.rect.left < 0:
        s2.animations.set("WALK_R")
        s2.dx = 1
    elif s2.rect.right >= window.rect().w:
        s2.animations.set("WALK_L")
        s2.dx = -1
    s2.rect.move(s2.dx, 0)
    s2.update()

    window.fill(WHITE)
    s1.draw(window)
    s2.draw(window)

window.loop(main)
