import random

import pygame

from shared.sprite  import Sprite
from empire_city.common import asset_path

def get_time(): return pygame.time.get_ticks() // 1000

class Enemies:
    street_mob = Sprite.from_paths([asset_path("bandit_rue.png")])

    def __init__(self, bg):
        self.bg = bg
        self.kill()

    def generate_street(self):
        self.enemy = Sprite(self.street_mob.images)
        self.enemy.rect.move_ip(
            random.randint(100, self.bg.rect.width - self.enemy.rect.width - 100),
            self.bg.rect.height - self.enemy.rect.height - 10
        )

    # Generates a new enemy.
    def next(self):
        self.generate_street()

    def kill(self):
        self.enemy = None
        self.t0 = get_time()

    # Generates a new enemy 3 seconds after the previous one has been killed.
    def update(self):
        if (self.enemy is None) and (get_time() - self.t0 >= 3): self.next()

    def draw(self):
        if self.enemy is not None: self.bg.image.blit(
            source = self.enemy.image,
            dest   = self.enemy.rect
        )
