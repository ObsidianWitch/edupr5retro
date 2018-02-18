import random

import pygame

import shared.math
from shared.sprite import Sprite
from empire_city.common import asset_path, get_time

class Explosion(Sprite):
    image0 = Sprite.from_paths([asset_path("bang.png")]).images

    def __init__(self, center):
        Sprite.__init__(self, self.image0)
        self.rect.center = center
        self.t0 = get_time()

    def update(self):
        if (get_time() - self.t0 >= 2): self.kill()

class Player:
    def __init__(self, camera):
        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg

        self.crosshair = Sprite.from_paths([asset_path("viseur.png")])
        self.crosshair.rect.center = self.window.rect.center
        self.ammunition = Sprite.from_paths([asset_path("bullet.png")])
        self.ammunition.scale_ip(0.5)
        self.ammunition.rect.bottomleft = self.window.rect.bottomleft
        self.explosions = pygame.sprite.Group()

        self.speed = 10
        self.ammunitions = 12

    def move(self, collisions_vec):
        move_vec = shared.math.Directions(
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
        if self.ammunitions <= 0: return

        shoot = self.window.keydown(pygame.K_SPACE)
        if not shoot: return

        self.ammunitions -= 1
        self.crosshair.rect.move_ip(
            random.randint(-2, 2),
            random.randint(-2, 2)
        )
        self.explosions.add(Explosion(
            self.camera.bg_space(self.crosshair.rect.center)
        ))

        killed = target.killcollide(
            self.camera.bg_space(self.crosshair.rect.center)
        )
        if killed: self.ammunitions += 2

    def update(self, collisions_vec, target):
        self.move(collisions_vec)
        self.shoot(target)
        self.explosions.update()

    def draw_bg(self):
        self.explosions.draw(self.bg.image)

    def draw_screen(self):
        self.window.screen.blit(self.crosshair.image, self.crosshair.rect)

        for a in range(self.ammunitions):
            self.window.screen.blit(
                self.ammunition.image, self.ammunition.rect.move(
                    a * self.ammunition.rect.width, 0
                )
            )
