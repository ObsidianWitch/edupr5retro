import types
import pygame

import shared.transform
import shared.collisions
from shared.image import Image
from shared.animated_sprite import AnimatedSprite, Animations
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

    def __init__(self, window, bg, position):
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
                    "BUILD_L": range(56, 72),
                    "BUILD_R": range(56 + 133, 72 + 133),
                    "DIGV_L":  range(72, 88),
                    "DIGV_R":  range(72 + 133, 88 + 133),
                    "DIGH_L":  range(88, 100),
                    "DIGH_R":  range(88 + 133, 100 + 133),
                    "MINE_L":  range(100, 117),
                    "MINE_R":  range(100 + 133, 117 + 133),
                    "DEAD_L":  range(117, 133),
                    "DEAD_R":  range(117 + 133, 133 + 133),
                },
                period  = 100,
            ),
            position = position
        )
        self.colorkey(pygame.Color("black"))

        self.actions = Actions(self)
        self.state = STATES.START

    @property
    def bounding_rect(self):
        dx = self.actions.walk.dx
        rect = self.rect.copy()
        rect.width //= 2
        if dx > 0: rect.left += rect.width
        return rect

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

    def collisions(self, surface):
        directions = shared.collisions.pixel_mid(
            surface, self.bounding_rect, pygame.Color("black")
        ).invert()

        outside = (None in directions)
        directions.replace(None, True)

        fall = not directions.down

        dx = self.actions.walk.dx
        side = (directions.vec[0] == dx)

        return types.SimpleNamespace(
            outside = outside,
            fall    = fall,
            side    = side,
        )

    def update(self, new_action):
        collisions_all = self.collisions(self.bg.current)
        collisions_bg  = self.collisions(self.bg.original)

        if self.state == STATES.START:
            self.actions.walk.start()
            self.actions.fall.start()
            self.state = STATES.FALL

        elif self.state == STATES.WALK:
            if collisions_all.fall:
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
            elif new_action == STATES.BUILD:
                self.state = new_action
                self.actions.build.start()
            elif new_action == STATES.DIGV:
                self.state = new_action
                self.actions.digv.start()
            elif new_action == STATES.DIGH:
                self.state = new_action
                self.actions.digh.wait()
            elif new_action == STATES.MINE:
                self.state = new_action
                self.actions.mine.wait()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == STATES.FALL:
            if collisions_all.fall:
                self.actions.fall.run()
            elif self.actions.fall.dead:
                self.state = STATES.DEAD
                self.actions.dead.start()
            else:
                self.actions.fall.clamp()
                self.state = STATES.WALK

        elif self.state == STATES.FLOAT:
            if collisions_all.fall:
                self.actions.float.run()
            elif self.actions.float.enabled:
                self.state = STATES.WALK
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == STATES.STOP:
            self.actions.stop.run()

        elif self.state == STATES.BOMB:
            if self.actions.bomb.explode:
                self.actions.bomb.run()
            elif self.actions.bomb.timer.finished:
                self.actions.bomb.start()
            elif collisions_all.fall:
                self.actions.bomb.start()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == STATES.BUILD:
            if self.actions.build.finished or collisions_bg.side:
                self.state = STATES.WALK
            else:
                self.actions.build.run()

        elif self.state == STATES.DIGV:
            if (not collisions_bg.fall) and (not collisions_bg.outside):
                self.actions.digv.run()
            else:
                self.state = STATES.WALK

        elif self.state == STATES.DIGH:
            if collisions_bg.side and (not collisions_bg.outside):
                self.actions.digh.run()
            elif collisions_all.fall:
                self.state = STATES.WALK
            elif self.actions.digh.enabled:
                self.state = STATES.WALK
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == STATES.MINE:
            if (
                collisions_bg.side
                and (not collisions_bg.fall)
                and (not collisions_bg.outside)
            ):
                self.actions.mine.run()
            elif (collisions_all.fall) or (self.actions.mine.enabled):
                self.state = STATES.WALK
            else:
                self.actions.walk.run(collisions_all)

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
