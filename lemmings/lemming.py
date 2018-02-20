import enum
import types
import pygame

from shared.animated_sprite import AnimatedSprite, Animations
from lemmings.common import asset_path

STATES = enum.Enum("STATES", "WALK FALL")

class Fall:
    def __init__(self, lemming):
        self.lemming = lemming
        self.start()

    def start(self):
        self.lemming.sprite.animations.set("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.sprite.rect.move_ip(0, 3)
        self.fallcount += 3

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
                default = "FALL",
                period  = 100,
            ),
            position = (250, 100)
        )
        self.sprite.colorkey(pygame.Color("black"))

        self.behaviours = types.SimpleNamespace(
            fall = Fall(self),
        )

        self.state = STATES.FALL

    def update(self):
        self.sprite.update()

        if self.state == STATES.FALL:
            self.behaviours.fall.run()

    def draw(self): self.sprite.draw(self.window.screen)
