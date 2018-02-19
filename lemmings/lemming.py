import enum
import pygame

from lemmings.common import asset_path

class Lemming:
    STATES = enum.Enum("STATES", "WALKING FALLING STOP DEAD")

    def __init__(self, window):
        self.window = window

        self.x  = 250
        self.y  = 100
        self.dx = -1

        self.state     = self.STATES.FALLING
        self.fallcount = 0

        self.spritesheet = pygame.image.load(asset_path("planche.png"))
        self.spritesheet.set_colorkey(pygame.Color("black"))

        self.walking_animation = self.chargeSerieSprites(0)
        self.falling_animation  = self.chargeSerieSprites(1)

    def chargeSerieSprites(self, id):
        sprite_width = 30
        sprite = []
        for i in range(18):
            spr = self.spritesheet.subsurface(
                (sprite_width * i, sprite_width * id, sprite_width, sprite_width)
            )
            test = spr.get_at((10,10))
            if (test != (255,0,0,255)): sprite.append(spr)
        return sprite

    def falling(self):
        self.y += 3
        self.fallcount += 3

    def update(self):
        if self.state == self.STATES.FALLING: self.falling()

    def draw(self):
        time = int(pygame.time.get_ticks() / 100)

        if self.state == self.STATES.FALLING:
            i = time % len(self.falling_animation)
            self.window.screen.blit(
                self.falling_animation[i],
                (self.x, self.y)
            )
