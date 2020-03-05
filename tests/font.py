from src.constants import *
from src.window import Window
from src.font import Font

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)

font1 = Font(size = 74)
font2 = window.fonts[4]

txt1 = font1.render(
    text = "Example 1",
)
txt1_rect = txt1.rect()
txt1_rect.ct = window.rect().ct

txt2 = font1.render(
    text      = "Example 2",
    antialias = False,
    color     = RED,
    bgcolor   = BLACK,
)
txt2_rect = txt2.rect()
txt2_rect.cc = window.rect().cc

txt3 = font2.render(
    text      = "Example 3",
    antialias = True,
    color     = BLUE,
    bgcolor   = GREEN,
)
txt3_rect = txt3.rect()
txt3_rect.cb = window.rect().cb

def main():
    window.fill(WHITE) \
          .draw_img(txt1, txt1_rect.lt) \
          .draw_img(txt2, txt2_rect.lt) \
          .draw_img(txt3, txt3_rect.rt)

window.loop(main)
