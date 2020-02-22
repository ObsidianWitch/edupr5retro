from pr5retro.constants import *
from pr5retro.window import Window
from pr5retro.font import Font

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
txt1_rect.midtop = window.rect().midtop

txt2 = font1.render(
    text      = "Example 2",
    antialias = True,
    color     = RED,
    bgcolor   = BLACK,
)
txt2_rect = txt2.rect()
txt2_rect.center = window.rect().center

txt3 = font2.render(
    text      = "Example 3",
    antialias = True,
    color     = BLUE,
    bgcolor   = GREEN,
)
txt3_rect = txt3.rect()
txt3_rect.midbottom = window.rect().midbottom

def main():
    window.fill(WHITE) \
          .draw_img(txt1, txt1_rect) \
          .draw_img(txt2, txt2_rect.topleft) \
          .draw_img(txt3, txt3_rect.topright)

window.loop(main)
