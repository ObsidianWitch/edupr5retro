import enum
import pygame

from shared.animated_sprite import AnimatedSprite, Animations
from lemmings.common import asset_path

STATES = enum.Enum("STATES", "WALK FALL STOP DEAD")

class StateFall:
    ID = STATES.FALL

    def __init__(self, lemming):
        self.lemming = lemming
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

        self.state = StateFall(self)

    def update(self):
        self.sprite.update()

        if self.state.ID == STATES.FALL: self.state.run()

    def draw(self): self.sprite.draw(self.window.screen)
