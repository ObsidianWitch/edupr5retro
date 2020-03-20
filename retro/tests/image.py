import sys
from retro.src import retro
from retro.tests.path import assets

def TestDraw():
    def draw(target):
        target.draw_line(
            color     = retro.GREEN,
            start_pos = (10, 0),
            end_pos   = (60, 30),
            width     = 5,
        )
        target.draw_rect(
            color = retro.BLACK,
            rect  = (10, 40, 50, 20),
            width = 2,
        )
        target.draw_rect(
            color = retro.BLACK,
            rect  = (10, 70, 50, 20),
        )
        target.draw_circle(
            color  = retro.BLUE,
            center = (50, 150),
            radius  = 40,
        )
        target.draw_circle(
            color  = retro.BLUE,
            center = (50, 250),
            radius  = 40,
            width   = 4,
        )

    return draw

def TestInit():
    s1 = retro.Image((100, 100))
    s1_rect = s1.rect()
    s1_rect.move_ip(100, 10)

    s2 = retro.Image.from_path(assets("img.png"))
    s2_rect = s2.rect()
    s2_area = retro.Rect(20, 10, 30, 30)
    s2_rect.move_ip(100, 110)

    s3 = retro.Image.from_path(assets("trap.png"))
    s3_rect = s3.rect()
    s3_rect.move_ip(100, 150)

    s4 = s3.copy()
    s4_rect = s3_rect.copy()
    s4_rect.move_ip(50, 0)

    s5 = s4
    s5_rect = s4_rect.copy()
    s5_rect.move_ip(50, 0)
    s5.draw_line(retro.GREEN, (0, 0), (30, 30))

    subimages = retro.Image.from_spritesheet(
        path = assets("spritesheet.png"),
        sprite_size = (30, 30),
        discard_color = retro.RED,
    )

    def draw(target):
        target.draw_img(s1, s1_rect.topleft)
        target.draw_img(s2, s2_rect.topleft, s2_area)
        target.draw_img(s3, s3_rect.topleft)
        target.draw_img(s4, s4_rect.topleft)
        target.draw_img(s5, s5_rect.topleft)

        for i, s in enumerate(subimages):
            x = (i % 10) * (s.rect().width + 10) + 230
            y = (i // 10) * (s.rect().height + 10)
            target.draw_img(s, (x, y))

    return draw

def TestTransform():
    obj1 = retro.Image((50, 50)).draw_line(
        color     = retro.GREEN,
        start_pos = (0, 0),
        end_pos   = (25, 25),
        width     = 5,
    )
    obj1_rect = obj1.rect()
    obj1_rect.move_ip(10, 300)

    obj2 = obj1.copy()
    obj2.colorkey(color = retro.BLACK)
    obj2.flip(x = True, y = False)
    obj2_rect = obj2.rect()
    obj2_rect.topleft = obj1_rect.topright

    obj3 = retro.Image((50, 50))
    obj3.fill(color = retro.BLUE)
    obj3.draw_rect(
        color = retro.WHITE,
        rect  = retro.Rect(10, 10, 25, 25),
        width = 4,
    )
    obj3.rotate(45)
    obj3_rect = obj3.rect()
    obj3_rect.topleft = obj1_rect.bottomleft

    obj4 = obj3.copy().resize((25, 25))
    obj4_rect = obj4.rect()
    obj4_rect.topleft = obj3_rect.topright

    obj5 = obj3.copy()
    obj5.scale(1.4)
    obj5_rect = obj5.rect()
    obj5_rect.topleft = obj3_rect.bottomleft

    def draw(target):
        target.draw_img(obj1, obj1_rect.topleft)
        target.draw_img(obj2, obj2_rect.topleft)
        target.draw_img(obj3, obj3_rect.topleft)
        target.draw_img(obj4, obj4_rect.topleft)
        target.draw_img(obj5, obj5_rect.topleft)

    return draw

# ---

window = retro.Window(
    title    = 'test',
    size     = (800, 600),
    headless = '--display' not in sys.argv,
)
test_draw = TestDraw()
test_init = TestInit()
test_tf = TestTransform()

def main(target):
    target.fill(retro.WHITE)
    test_draw(target)
    test_init(target)
    test_tf(target)

if window.headless:
    main(window)
    # window.save('out.png')
    assert window == retro.Image.from_path(assets('expectation_image.png'))
else:
    window.loop(lambda: main(window))
