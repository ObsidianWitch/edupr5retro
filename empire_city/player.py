import random

import pygame

import shared.math
from shared.sprite import Sprite
from empire_city.common import asset_path

class Player:
    def __init__(self, window, camera):
        self.window = window
        self.camera = camera

        self.crosshair = Sprite.from_paths([asset_path("viseur.png")])
        self.crosshair.rect.center = window.rect.center
        self.ammunition = Sprite.from_paths([asset_path("bullet.png")])
        self.ammunition.scale_ip(0.5)
        self.ammunition.rect.bottomleft = window.rect.bottomleft

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

        # Avoid shooting multiple times while holding space by using
        # `window.events` instead of `window.keys`.
        shoot = next(
            (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE
            for e in self.window.events),
            False
        )
        if not shoot: return

        self.ammunitions -= 1
        self.crosshair.rect.move_ip(
            random.randint(-2, 2),
            random.randint(-2, 2)
        )
        killed = target.killcollide(
            self.camera.bg_space(self.crosshair.rect.center)
        )
        if killed: self.ammunitions += 2

    def draw(self):
        self.window.screen.blit(self.crosshair.image, self.crosshair.rect)

        for a in range(self.ammunitions):
            self.window.screen.blit(
                self.ammunition.image, self.ammunition.rect.move(
                    a * self.ammunition.rect.width, 0
                )
            )
