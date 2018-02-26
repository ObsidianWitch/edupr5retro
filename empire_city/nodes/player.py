import random
import pygame

import shared.math
from shared.directions import Directions
from shared.sprite import Sprite
from shared.image import Image
from shared.timer import Timer
from empire_city.path import asset_path

class Ammunitions(Sprite):
    IMG = Image.from_path(asset_path("bullet.png"))

    def __init__(self, window):
        self.window = window

        Sprite.__init__(self, self.IMG)
        self.scale(0.5)
        self.rect.bottomleft = self.window.rect.bottomleft

        self.count = 12

    def draw(self):
        for i in range(self.count):
            self.rect.left = i * self.rect.width
            Sprite.draw(self, self.window.screen)

class Explosion(Sprite):
    IMG = Image.from_path(asset_path("bang.png"))

    def __init__(self, center):
        Sprite.__init__(self, self.IMG)
        self.rect.center = center
        self.timer = Timer(2)

    def update(self):
        if self.timer.finished: self.kill()

class Player:
    CROSSHAIR_IMG  = Image.from_path(asset_path("viseur.png"))
    HIDE_IMG       = Image.from_path(asset_path("hide.png"))

    def __init__(self, camera):
        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg

        self.crosshair = Sprite(self.CROSSHAIR_IMG)
        self.crosshair.rect.center = self.window.rect.center

        self.ammunitions = Ammunitions(self.window)

        self.hide = Sprite(self.HIDE_IMG)
        self.hide.rect.center = self.window.rect.center

        self.explosions = pygame.sprite.Group()

        self.speed = 10
        self.hidden = False

    def move(self, collisions_vec):
        move_vec = Directions(
            up    = self.window.keys[pygame.K_UP],
            down  = self.window.keys[pygame.K_DOWN],
            left  = self.window.keys[pygame.K_LEFT],
            right = self.window.keys[pygame.K_RIGHT],
        ).vec

        for i,_ in enumerate(move_vec):
            move_vec[i] -= collisions_vec[i]
            move_vec[i] = shared.math.clamp(move_vec[i], -1, 1)

        self.crosshair.rect.move_ip(
            move_vec[0] * self.speed,
            move_vec[1] * self.speed,
        )

    def shoot(self, target):
        if self.ammunitions.count <= 0: return
        if not self.window.keydown(pygame.K_SPACE): return

        self.ammunitions.count -= 1
        self.crosshair.rect.move_ip(
            random.randint(-2, 2),
            random.randint(-2, 2)
        )
        self.explosions.add(Explosion(
            self.camera.bg_space(self.crosshair.rect.center)
        ))

        killed = target.kill(
            self.camera.bg_space(self.crosshair.rect.center)
        )
        if killed ==  1: self.ammunitions.count += 2
        if killed == -1: self.ammunitions.count -= 3

    def update(self, collisions_vec, target):
        self.move(collisions_vec)
        self.shoot(target)
        self.explosions.update()
        self.hidden = self.window.keys[pygame.K_RETURN]

    def draw_bg(self):
        self.explosions.draw(self.bg.current)

    def draw_screen(self):
        self.crosshair.draw(self.window.screen)

        if self.hidden: self.hide.draw(self.window.screen)

        self.ammunitions.draw()
