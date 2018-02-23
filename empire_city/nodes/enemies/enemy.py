import pygame

from shared.sprite import Sprite
from shared.timer  import Timer

class Enemy(Sprite):
    def __init__(self, camera, image):
        Sprite.__init__(self, image)

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
            )
        )

    def draw_bg(self):
        if not self.alive: return
        self.draw(self.bg.image)

    def draw_screen(self):
        if not self.alive: return
        self.draw_shoot_timer()
