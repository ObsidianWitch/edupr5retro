import enum
import pygame

from shared.sprite import Sprite
from lemmings.path import asset_path

STATES = enum.Enum("STATES", "START WALK FALL STOP DIGV DEAD")

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.dx = -1

    def run(self, collision_vec):
        if self.dx == collision_vec[0]:
            self.dx *= -1
            self.lemming.rect.move_ip(-self.dx * 20, 0)

        self.lemming.set_animation("WALK")
        self.lemming.rect.move_ip(self.dx, 0)

class Fall:
    @property
    def dead(self): return (self.fallcount >= 100)

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.rect.move_ip(0, 3)
        self.fallcount += 3

class Stop:
    ICON  = Sprite.path_to_image(asset_path("ui_stop.png"))
    STATE = STATES.STOP

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("STOP")

    def run(self): pass

class DigV:
    ICON  = Sprite.path_to_image(asset_path("ui_digv.png"))
    STATE = STATES.DIGV

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("DIGV")

    def run(self):
        rect = self.lemming.rect.copy()
        rect.top = rect.bottom
        rect.left += 10 if self.lemming.actions.walk.dx > 0 else 0
        rect.size = (20, 1)

        self.lemming.bg.original.fill(
            pygame.Color("black"), rect
        )
        self.lemming.rect.move_ip(0, 1)

class Dead:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("DEAD")

    def run(self):
        if self.lemming.animations.finished: self.lemming.kill()

class Actions:
    USABLE = (Stop, DigV)

    def __init__(self, lemming):
        self.walk = Walk(lemming)
        self.fall = Fall(lemming)
        self.stop = Stop(lemming)
        self.digv = DigV(lemming)
        self.dead = Dead(lemming)
