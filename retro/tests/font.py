import sys
from src.constants import *
from src.window import Window
from src.font import Font
from src.image import Image
from tests.path import assets

def TestFont(target):
    txt1 = Font(size = 64).render(
        text = "Example 1",
    )
    txt1_rect = txt1.rect()

    txt2 = Font(size = 32).render(
        text    = "Example 2",
        color   = RED,
        bgcolor = BLACK,
    )
    txt2_rect = txt2.rect()
    txt2_rect.center = target.rect().center

    txt3 = Font(size = 16).render(
        text      = "Example 3",
        antialias = True,
        color     = BLUE,
        bgcolor   = GREEN,
    )
    txt3_rect = txt3.rect()
    txt3_rect.bottomright = target.rect().bottomright

    def draw():
        target.fill(WHITE)
        target.draw_img(txt1, txt1_rect.topleft)
        target.draw_img(txt2, txt2_rect.topleft)
        target.draw_img(txt3, txt3_rect.topleft)

    return draw

window = Window(
    title    = 'test',
    size     = (640, 480),
    headless = '--display' not in sys.argv,
)
test_font = TestFont(window)

if window.headless:
    test_font()
    # window.save('out.png')
    assert window == Image.from_path(assets('expectation_font.png'))
else:
    window.loop(test_font)
