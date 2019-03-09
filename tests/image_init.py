import os
import itertools
from src.constants import *
from src.window import Window
from src.image import Image
from src.rect import Rect

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)

PALETTE = {
    ' ': BLACK,
    'W': WHITE,
    'R': RED,
    'G': GREEN,
    'B': BLUE,
    'C': CYAN,
    'Y': YELLOW,
}

ASCII_IMG = (
    '                    ',
    '                    ',
    '          RRRR      ',
    '        RRYRRRR     ',
    '       RRYRR   R    ',
    '       RYYRRRR      ',
    '     RRRYYRYYRRR    ',
    '    RYRRYRYYYYRRR   ',
    '    RYYYYRRRYYYRR   ',
    '    RRYYRRRRYRRRR   ',
    '  R RRYRRRRRRYRR    ',
    '  R  RRYRRRRRYR     ',
    '  RRRRYYYRRRYYYR    ',
    '   RRRRYYYRYRRYR    ',
    '     RRRRRYYRRRR    ',
    '    R  RRYYRR RR    ',
    '     RRRRRRR  R     ',
    '       RRRR  R      ',
    '                    ',
    '                    ',
)


s1 = Image((100, 100))
s1_rect = s1.rect()
s1_rect.move(10, 10)
print(s1.rect)
print(s1_rect)

s2 = Image.from_path(os.path.join(
    "tests", "data", "img.png"
))
s2_rect = s2.rect()
s2_rect.move(10, 110)
s2_area = Rect(20, 10, 30, 30)

s3 = Image.from_ascii(ASCII_IMG, PALETTE)
s3_rect = s3.rect()
s3_rect.move(10, 150)

s4 = s3.copy()
s4_rect = s3_rect.copy()
s4_rect.move(50, 0)

s5 = s4
s5_rect = s4_rect.copy()
s5_rect.move(50, 0)
s5.draw_line(GREEN, (0, 0), (30, 30))

subimages = Image.from_spritesheet(
    path = os.path.join(
        "tests", "data", "spritesheet.png"
    ),
    sprite_size = (30, 30),
    discard_color = RED,
)
subimages = list(itertools.chain(*subimages))

def main():
    window.fill(WHITE) \
          .draw_img(s1, s1_rect) \
          .draw_img(s2, s2_rect, s2_area) \
          .draw_img(s3, s3_rect) \
          .draw_img(s4, s4_rect) \
          .draw_img(s5, s5_rect)

    for i, s in enumerate(subimages):
        x = (i % 10) * (s.rect().width + 10) + 150
        y = (i // 10) * (s.rect().height + 10)
        window.draw_img(s, (x, y))

    print(window.events.mouse_pos())

window.loop(main)
