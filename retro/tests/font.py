import sys
from retro.src import retro
from retro.tests.path import assets

def TestFont(target):
    txt1 = retro.Font(size = 64).render(
        text = "Example 1",
    )
    txt1_rect = txt1.rect()

    txt2 = retro.Font(size = 32).render(
        text    = "Example 2",
        color   = retro.RED,
        bgcolor = retro.BLACK,
    )
    txt2_rect = txt2.rect()
    txt2_rect.center = target.rect().center

    txt3 = retro.Font(size = 16).render(
        text      = "Example 3",
        antialias = True,
        color     = retro.BLUE,
        bgcolor   = retro.GREEN,
    )
    txt3_rect = txt3.rect()
    txt3_rect.bottomright = target.rect().bottomright

    def draw():
        target.fill(retro.WHITE)
        target.draw_img(txt1, txt1_rect.topleft)
        target.draw_img(txt2, txt2_rect.topleft)
        target.draw_img(txt3, txt3_rect.topleft)

    return draw

window = retro.Window(
    title    = 'test',
    size     = (640, 480),
    headless = '--display' not in sys.argv,
)
test_font = TestFont(window)

if window.headless:
    test_font()
    # window.save(assets('expectation_font.png'))
    assert window == retro.Image.from_path(assets('expectation_font.png'))
else:
    window.loop(test_font)
