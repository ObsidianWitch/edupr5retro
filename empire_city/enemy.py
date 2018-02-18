import random

import pygame

from shared.sprite  import Sprite
from empire_city.common import asset_path, get_time

class Enemy:
    street_mob = Sprite.from_paths([asset_path("bandit_rue.png")])

    @property
    def alive(self): return self.mob is not None

    def __init__(self, camera):
        self.camera = camera
        self.bg = camera.bg
        self.kill()

    def generate_street(self):
        mob = Sprite(self.street_mob.images)
        mob.rect.move_ip(
            random.randint(100, self.bg.rect.width - mob.rect.width - 100),
            self.bg.rect.height - mob.rect.height - 10
        )
        self.mob = mob

    # Generates a new enemy.
    def next(self):
        self.generate_street()

    def kill(self):
        self.mob = None
        self.t0 = get_time()

    def killcollide(self, p):
        killed = (self.alive and self.mob.rect.collidepoint(p))
        if killed: self.kill()
        return killed

    # Generates a new enemy 3 seconds after the previous one has been killed.
    def update(self):
        if not self.alive and (get_time() - self.t0 >= 3): self.next()

    def draw_bg(self):
        if self.alive: self.bg.image.blit(self.mob.image, self.mob.rect)
