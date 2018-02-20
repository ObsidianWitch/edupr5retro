import enum
import types
import pygame

from shared.collisions import pixel_collision_mid
from shared.animated_sprite import AnimatedSprite, Animations
from lemmings.common import asset_path

STATES = enum.Enum("STATES", "START WALK FALL")

class Fall:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.sprite.animations.start("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.sprite.rect.move_ip(0, 3)
        self.fallcount += 3

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.dx = -1

    def run(self):
        if self.dx < 0: self.lemming.sprite.animations.set("WALK_L")
        self.lemming.sprite.rect.move_ip(self.dx, 0)

class Lemming:
    lemming_imgs = AnimatedSprite.spritesheet_to_images(
        path          = asset_path("planche.png"),
        sprite_size   = (30, 30),
        discard_color = pygame.Color("red"),
    )

    def __init__(self, window):
        self.window = window

        self.sprite = AnimatedSprite(
            images = self.lemming_imgs,
            animations = Animations(
                data = {
                    "WALK_L": range(0, 8),
                    "FALL"  : range(8, 12),
                },
                default = "WALK_L",
                period  = 100,
            ),
            position = (250, 100)
        )
        self.sprite.colorkey(pygame.Color("black"))

        self.behaviours = types.SimpleNamespace(
            walk = Walk(self),
            fall = Fall(self),
        )

        self.state = STATES.START

    def update(self):
        self.sprite.update()

        if self.state == STATES.START:
            self.behaviours.walk.start()
            self.state = STATES.WALK

        if self.state == STATES.WALK:
            fall = pixel_collision_mid(
                self.window.screen, self.sprite.rect, pygame.Color("black")
            ).down

            if fall:
                self.state = STATES.FALL
                self.behaviours.fall.start()
                return

            self.behaviours.walk.run()

        if self.state == STATES.FALL:
            walk = not pixel_collision_mid(
                self.window.screen, self.sprite.rect, pygame.Color("black")
            ).down
            
            if walk:
                self.state = STATES.WALK
                return

            self.behaviours.fall.run()

    def draw(self): self.sprite.draw(self.window.screen)
