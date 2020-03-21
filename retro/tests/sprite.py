import os
from retro.src import retro
from retro.tests.path import assets

window = retro.Window(
    title = "window",
    size  = (320, 240),
    fps   = 60,
)

s1 = retro.Sprite.from_path(assets("img.png"))
s1.dy = 1

s2 = retro.Sprite.from_spritesheet(
    path = assets("spritesheet.png"),
    animations = retro.Animations(
        frame_size = (30, 30),
        period = 100,
        WALK_R = (tuple(reversed(range(0, 8))), 11),
        WALK_L = (range(0, 8), 0),
    ),
)
s2.dx = 1

def main():
    if s1.rect.top < 0:
        s1.dy = 1
    elif s1.rect.bottom >= window.rect().h:
        s1.dy = -1
    s1.rect.move_ip(0, s1.dy)

    if s2.rect.left < 0:
        s2.animations.set("WALK_R")
        s2.dx = 1
    elif s2.rect.right >= window.rect().w:
        s2.animations.set("WALK_L")
        s2.dx = -1
    s2.rect.move_ip(s2.dx, 0)

    window.fill(retro.WHITE)
    s1.draw(window)
    s2.draw(window, area = retro.Rect(15, 10, 100, 100))

window.loop(main)
