import enum
import pygame

from shared.animated_sprite import AnimatedSprite, Animations
import shared.transform
import shared.collisions
from lemmings.characters.actions import Actions
from lemmings.common import asset_path

STATES = enum.Enum("STATES", "START WALK FALL STOP DEAD")

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

        self.actions = Actions(self)
        self.state = STATES.START

    def update(self, new_action):
        collisions = shared.collisions.pixel_collision_mid(
            self.bg.current, self.rect, pygame.Color("black")
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
            AnimatedSprite.draw(self, self.bg.current)

    def draw_screen(self):
        if self.state != STATES.STOP:
            AnimatedSprite.draw(self, self.window.screen)
