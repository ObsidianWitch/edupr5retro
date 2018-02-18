import random
import pygame

from shared.sprite import Sprite
from shared.timer  import Timer
from empire_city.common import asset_path

class Enemy:
    street_mob = Sprite.from_paths([asset_path("bandit_rue.png")])

    @property
    def alive(self): return self.mob is not None

    def __init__(self, camera):
        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg
        self.font   = pygame.font.SysFont(None, 24)

        self.repop_timer = Timer(3)
        self.shoot_timer = Timer(3)

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
        self.shoot_timer.restart()

    def kill(self):
        self.mob = None
        self.repop_timer.restart()

    def killcollide(self, p):
        killed = (self.alive and self.mob.rect.collidepoint(p))
        if killed: self.kill()
        return killed

    def shoot(self, target):
        if not self.shoot_timer.finished: return
        self.shoot_timer.restart()
        if target.hidden: return
        target.ammunitions -= 3

    # Generates a new enemy 3 seconds after the previous one has been killed.
    def update(self, target):
        if not self.alive and self.repop_timer.finished: self.next()
        if self.alive: self.shoot(target)

    def draw_bg(self):
        if self.alive: self.bg.image.blit(self.mob.image, self.mob.rect)

    def draw_screen(self):
        if not self.alive: return

        shoot_timer_surface = self.font.render(
            f"{self.shoot_timer.remaining}", # text
            False,                           # antialias
            pygame.Color("white")            # color
        )
        self.window.screen.blit(
            shoot_timer_surface,
            shoot_timer_surface.get_rect(
                midbottom = self.window.rect.midbottom
            ).move(0, 0)
        )
