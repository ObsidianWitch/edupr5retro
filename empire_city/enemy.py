import random
import enum
import pygame

from shared.sprite import Sprite
from shared.timer  import Timer
from empire_city.common import asset_path

# Enemy generator.
class Enemies:
    street_images = Sprite.from_paths([
        asset_path("bandit_rue.png"),
        asset_path("bandit_rue2.png"),
        asset_path("bandit_rue4.png"),
    ]).images

    def __init__(self, camera):
        self.camera = camera
        self.bg = camera.bg

        self.generators = (
            self.new_street_mob,
        )

        self.next()
        self.mob.alive = False

        self.repop_timer = Timer(3)

    def street_position(self, sprite):
        sprite.rect.bottom = self.bg.rect.bottom - 10
        sprite.rect.left = random.randint(
            100,
            self.bg.rect.width - sprite.rect.width - 100
        )

    def new_street_mob(self):
        mob = Enemy(self.camera, [random.choice(self.street_images)])
        self.street_position(mob)
        return mob

    def next(self):
        self.mob = random.choice(self.generators)()

    def kill(self, p):
        killed = self.mob.kill(p)
        if killed: self.repop_timer.restart()
        return killed

    def update(self, target):
        repop = (
            not self.mob.alive
            and self.repop_timer.finished
        )
        if repop: self.next()

        self.mob.update(target)

    def draw_bg(self):
        self.mob.draw_bg()

    def draw_screen(self):
        self.mob.draw_screen()

class Enemy(Sprite):
    def __init__(self, camera, images):
        Sprite.__init__(self, images)

        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg

        self.alive = True
        self.shoot_timer = Timer(3)

    def kill(self, p):
        killed = (self.alive and self.rect.collidepoint(p))
        if killed: self.alive = False
        return killed

    def shoot(self, target):
        if not self.shoot_timer.finished: return
        self.shoot_timer.restart()
        if target.hidden: return
        target.ammunitions -= 3

    def update(self, target):
        if not self.alive: return
        self.shoot(target)

    def draw_shoot_timer(self):
        if not self.alive: return

        shoot_timer_surface = self.window.fonts[1].render(
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

    def draw_bg(self):
        if not self.alive: return
        self.draw(self.bg.image)

    def draw_screen(self):
        if not self.alive: return
        self.draw_shoot_timer()
