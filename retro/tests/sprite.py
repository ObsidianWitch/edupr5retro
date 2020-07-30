import sys
from retro.src import retro
from retro.tests.path import assets

def TestSprite(target):
    s1 = retro.Sprite.from_path(assets('img.png'))
    s1.rect1 = s1.rect.copy()
    s1.rect1.top = s1.rect.bottom + 2

    s2 = retro.Sprite.from_spritesheet(
        path = assets('spritesheet.png'),
        animations = retro.Animations(
            frame_size = (30, 30),
            period = 100,
            WALK_R = (tuple(reversed(range(0, 8))), 11),
        ),
    )
    s2.rect.left = s1.rect.right
    s2.rect1 = s2.rect.copy()
    s2.rect1.top = s2.rect.bottom + 2

    s3 = retro.Sprite.from_path(assets('trap.png'))
    s3.rect.left = s2.rect.right
    s3.dy = 1

    def update():
        if s3.rect.top < 0 or s3.rect.top > 50:
            s3.dy *= -1
        s3.rect.y += s3.dy

        target.fill(retro.WHITE)
        s1.draw(target)
        s1.draw(target,
            position = s1.rect1.topleft,
            area = retro.Rect(10, 10, 30, 30))
        s2.draw(target)
        s2.draw(target,
            position = s2.rect1.topleft,
            area = retro.Rect(0, 10, 1000, 1000))
        s3.draw(target)

    return update

window = retro.Window(
    title='sprite', size=(320, 240), ups=30, fps=30,
    headless='--interactive' not in sys.argv,
)
test_sprite = TestSprite(window)

if window.headless:
    for _ in range(10): test_sprite()
    # window.save(assets('expectation_sprite.png'))
    assert window == retro.Image(assets('expectation_sprite.png'))
else:
    window.loop(None, test_sprite)
