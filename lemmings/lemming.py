import enum
import types
import pygame

import shared.transform
import shared.collisions
from shared.animated_sprite import AnimatedSprite, Animations
from lemmings.common import asset_path

STATES = enum.Enum("STATES", "START WALK FALL STOP DEAD")

class Fall:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.rect.move_ip(0, 3)
        self.fallcount += 3
        return (self.fallcount >= 100)

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.dx = -1

    def run(self, collision_vec):
        if self.dx == collision_vec[0]:
            self.dx *= -1
            self.lemming.rect.move_ip(-self.dx * 20, 0)

        if self.dx < 0:   self.lemming.animations.set("WALK_L")
        elif self.dx > 0: self.lemming.animations.set("WALK_R")

        self.lemming.rect.move_ip(self.dx, 0)

class Dead:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("DEAD")

    def run(self):
        if self.lemming.animations.finished: self.lemming.kill()

class Stop:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("STOP")

    def run(self): pass

class Lemming(AnimatedSprite):
    lemming_imgs = AnimatedSprite.spritesheet_to_images(
        path          = asset_path("planche.png"),
        sprite_size   = (30, 30),
        discard_color = pygame.Color("red"),
    )
    lemming_imgs += shared.transform.flip_n(
        surfaces = lemming_imgs[0:8],
        xflip    = True,
        yflip    = False
    )

    def __init__(self, window, bg):
        self.window = window
        self.bg = bg

        AnimatedSprite.__init__(
            self       = self,
            images     = self.lemming_imgs,
            animations = Animations(
                data = {
                    "WALK_L": range(0, 8),
                    "WALK_R": range(133, 141),
                    "FALL"  : range(8, 12),
                    "STOP"  : range(26, 42),
                    "DEAD"  : range(117, 133),
                },
                period  = 100,
            ),
            position = (250, 100)
        )
        self.colorkey(pygame.Color("black"))

        self.actions = types.SimpleNamespace(
            walk = Walk(self),
            fall = Fall(self),
            stop = Stop(self),
            dead = Dead(self),
        )

        self.state = STATES.START

    def update(self, new_action):
        collisions = shared.collisions.pixel_collision_mid(
            self.bg, self.rect, pygame.Color("black")
        ).invert()

        if self.state == STATES.START:
            self.actions.walk.start()
            self.actions.fall.start()
            self.state = STATES.FALL

        if self.state == STATES.WALK:
            self.actions.walk.run(collisions.vec)
            fall = not collisions.down
            if fall:
                self.state = STATES.FALL
                self.actions.fall.start()
            elif new_action == STATES.STOP:
                self.state = new_action
                self.actions.stop.start()

        if self.state == STATES.FALL:
            dead = self.actions.fall.run()
            walk = collisions.down
            if dead and walk:
                self.state = STATES.DEAD
                self.actions.dead.start()
            elif not dead and walk:
                self.state = STATES.WALK

        if self.state == STATES.STOP:
            self.actions.stop.run()

        if self.state == STATES.DEAD:
            self.actions.dead.run()

        AnimatedSprite.update(self)

    def draw_bg(self):
        if self.state == STATES.STOP:
            AnimatedSprite.draw(self, self.bg)

    def draw_screen(self):
        if self.state != STATES.STOP:
            AnimatedSprite.draw(self, self.window.screen)
