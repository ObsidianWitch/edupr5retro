import random
import shared.retro as retro
import shared.math
from shared.directions import Directions
from shared.sprite import Sprite
from shooter.path import asset

class Crosshair(Sprite):
    IMG = retro.Image.from_path(asset("crosshair.png"))

    def __init__(self, window):
        self.window = window

        Sprite.__init__(self, self.IMG)
        self.rect.center = self.window.rect().center

        self.speed = 10

    def scroll_vec(self):
        p = self.rect.center
        offset = 20
        w = self.window.rect().w
        h = self.window.rect().h
        return Directions(
            up    = (0 <= p[1] <= offset),
            down  = (h - offset <= p[1] <= h),
            left  = (0 <= p[0] <= offset),
            right = (w - offset <= p[0] <= w),
        ).vec

    def move(self, camera):
        scroll_vec = self.scroll_vec()

        # move crosshair
        key_hold = self.window.events.key_hold
        move_vec = Directions(
            up    = key_hold(retro.K_UP),
            down  = key_hold(retro.K_DOWN),
            left  = key_hold(retro.K_LEFT),
            right = key_hold(retro.K_RIGHT),
        ).vec

        for i,_ in enumerate(move_vec):
            move_vec[i] -= scroll_vec[i]
            move_vec[i] = shared.math.clamp(move_vec[i], -1, 1)

        self.rect.move(
            move_vec[0] * self.speed,
            move_vec[1] * self.speed,
        )

        # move camera
        camera.rect.move(
            scroll_vec[0] * self.speed,
            scroll_vec[1] * self.speed,
        )
        camera.rect.clamp(camera.bg.rect)

class Ammunitions(Sprite):
    IMG = retro.Image.from_path(asset("bullet.png"))
    IMG.scale(0.5)

    def __init__(self, window):
        self.window = window

        Sprite.__init__(self, self.IMG)
        self.rect.bottomleft = self.window.rect().bottomleft

        self.count = 12

    def draw(self, dest):
        for i in range(self.count):
            self.rect.left = i * self.rect.width
            Sprite.draw(self, dest)

class Hide(Sprite):
    IMG = retro.Image.from_path(asset("hide.png"))

    def __init__(self, window):
        self.window = window

        Sprite.__init__(self, self.IMG)
        self.rect.center = self.window.rect().center

        self.hidden = False

    def update(self):
        self.hidden = self.window.events.key_hold(retro.K_LSHIFT)

    def draw(self, dest):
        if self.hidden:
            Sprite.draw(self, dest)

class Explosion(Sprite):
    IMG = retro.Image.from_path(asset("bang.png"))

    def __init__(self, center):
        Sprite.__init__(self, self.IMG)
        self.rect.center = center
        self.timer = retro.Counter(2)

    def update(self):
        if self.timer.finished: self.kill()

class Player:
    def __init__(self, camera):
        self.camera = camera
        self.window = camera.window

        self.crosshair = Crosshair(self.window)
        self.ammunitions = Ammunitions(self.window)
        self.hide = Hide(self.window)
        self.explosions = retro.Group()

    def shoot(self, target):
        if self.ammunitions.count <= 0: return
        if self.hide.hidden: return
        if not self.window.events.key_press(retro.K_SPACE): return

        self.ammunitions.count -= 1
        self.crosshair.rect.move(
            random.randint(-2, 2),
            random.randint(-2, 2)
        )
        self.explosions.append(Explosion(
            self.camera.bg_space(self.crosshair.rect.center)
        ))

        killed = target.kill(
            self.camera.bg_space(self.crosshair.rect.center)
        )
        if   killed ==  1: self.ammunitions.count += 2
        elif killed == -1: self.ammunitions.count -= 3

    def update(self, target):
        self.crosshair.move(self.camera)
        self.shoot(target)
        self.explosions.update()
        self.hide.update()
