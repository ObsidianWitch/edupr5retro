import pygame

from shared.image import Image
from shared.animated_sprite import AnimatedSprite, Animations
import shared.transform
import shared.collisions
from lemmings.nodes.actions import Actions, STATES
from lemmings.path import asset_path

class Lemming(AnimatedSprite):
    lemming_imgs = Image.from_spritesheet_n(
        path          = asset_path("planche.png"),
        sprite_size   = (30, 30),
        discard_color = pygame.Color("red"),
    )
    lemming_imgs += shared.transform.flip_n(
        surfaces = lemming_imgs,
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
                    "WALK_L":  range(0, 8),
                    "WALK_R":  range(0 + 133, 8 + 133),
                    "FALL_L":  range(8, 12),
                    "FALL_R":  range(8 + 133, 12 + 133),
                    "FLOAT_L": range(20, 26),
                    "FLOAT_R": range(20 + 133, 26 + 133),
                    "STOP_L":  range(26, 42),
                    "STOP_R":  range(26 + 133, 42 + 133),
                    "BOMB_L":  range(42, 56),
                    "BOMB_R":  range(42 + 133, 56 + 133),
                    "DIGV_L":  range(72, 88),
                    "DIGV_R":  range(72 + 133, 88 + 133),
                    "DEAD_L":  range(117, 133),
                    "DEAD_R":  range(117 + 133, 133 + 133),
                },
                period  = 100,
            ),
            position = (250, 100)
        )
        self.colorkey(pygame.Color("black"))

        self.actions = Actions(self)
        self.state = STATES.START

    def set_animation(self, name):
        dx = self.actions.walk.dx
        if   dx < 0: self.animations.set(f"{name}_L")
        elif dx > 0: self.animations.set(f"{name}_R")
        else:        self.animations.set("NONE")

    def start_animation(self, name):
        dx = self.actions.walk.dx
        if   dx < 0: self.animations.start(f"{name}_L")
        elif dx > 0: self.animations.start(f"{name}_R")
        else:        self.animations.start("NONE")

    def update(self, new_action):
        collisions = shared.collisions.pixel_collision_mid(
            self.bg.current, self.rect, pygame.Color("black")
        ).invert()

        if self.state == STATES.START:
            self.actions.walk.start()
            self.actions.fall.start()
            self.state = STATES.FALL

        elif self.state == STATES.WALK:
            if not collisions.down:
                self.state = STATES.FALL
                self.actions.fall.start()
            elif new_action == STATES.FLOAT:
                self.state = new_action
                self.actions.float.wait()
            elif new_action == STATES.STOP:
                self.state = new_action
                self.actions.stop.start()
            elif new_action == STATES.BOMB:
                self.state = new_action
                self.actions.bomb.wait()
            elif new_action == STATES.DIGV:
                self.state = new_action
                self.actions.digv.start()
            else:
                self.actions.walk.run(collisions.vec)

        elif self.state == STATES.FALL:
            if not collisions.down:
                self.actions.fall.run()
            elif self.actions.fall.dead:
                self.state = STATES.DEAD
                self.actions.dead.start()
            else:
                self.state = STATES.WALK

        elif self.state == STATES.FLOAT:
            if not collisions.down:
                if not self.actions.float.enabled:
                    self.actions.float.start()
                self.actions.float.run()
            else:
                if self.actions.float.enabled:
                    self.state = STATES.WALK
                else:
                    self.actions.walk.run(collisions.vec)

        elif self.state == STATES.STOP:
            self.actions.stop.run()

        elif self.state == STATES.BOMB:
            if self.actions.bomb.explode:
                self.actions.bomb.run()
            elif self.actions.bomb.timer.finished:
                self.actions.bomb.start()
            elif not collisions.down:
                self.actions.fall.run()
            else:
                self.actions.walk.run(collisions.vec)

        elif self.state == STATES.DIGV:
            if collisions.down:
                self.actions.digv.run()
            else:
                self.state = STATES.WALK

        elif self.state == STATES.DEAD:
            self.actions.dead.run()

        AnimatedSprite.update(self)

    def draw_bg(self):
        if self.state != STATES.STOP: return

        AnimatedSprite.draw(self, self.bg.current)

    def draw_screen(self):
        if self.state == STATES.STOP: return
        elif self.state == STATES.BOMB:
            self.actions.bomb.draw_timer()

        AnimatedSprite.draw(self, self.window.screen)
