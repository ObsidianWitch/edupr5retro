import types
import shared.retro as retro
import shared.collisions
from lemmings.nodes.actions import Actions
from lemmings.path import asset

class Lemming(retro.AnimatedSprite):
    IMGS = retro.AnimatedSprite.from_spritesheet(
        path          = asset("planche.png"),
        sprite_size   = (30, 30),
        discard_color = retro.RED,
        animations    = retro.Animations(period = 0),
    ).images
    IMGS = [img.copy() for img in IMGS] \
         + [img.flip(x = True, y = False) for img in IMGS]

    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        retro.AnimatedSprite.__init__(
            self       = self,
            images     = self.IMGS,
            animations = retro.Animations(
                period  = 100,
                WALK_L  = range(0, 8),     WALK_R  = range(0 + 133, 8 + 133),
                FALL_L  = range(8, 12),    FALL_R  = range(8 + 133, 12 + 133),
                FLOAT_L = range(20, 26),   FLOAT_R = range(20 + 133, 26 + 133),
                STOP_L  = range(26, 42),   STOP_R  = range(26 + 133, 42 + 133),
                BOMB_L  = range(42, 56),   BOMB_R  = range(42 + 133, 56 + 133),
                BUILD_L = range(56, 72),   BUILD_R = range(56 + 133, 72 + 133),
                DIGV_L  = range(72, 88),   DIGV_R  = range(72 + 133, 88 + 133),
                DIGH_L  = range(88, 100),  DIGH_R  = range(88 + 133, 100 + 133),
                MINE_L  = range(100, 117), MINE_R  = range(100 + 133, 117 + 133),
                DEAD_L  = range(117, 133), DEAD_R  = range(117 + 133, 133 + 133),
            ),
        )
        self.colorkey(retro.BLACK)
        self.rect.topleft = position

        self.actions = Actions(self)
        self.state = None

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
            surface, self.bounding_rect, retro.BLACK
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
        collisions_all = self.collisions(self.bg.image)
        collisions_bg  = self.collisions(self.bg.original)

        if self.state is None:
            self.state = self.actions.fall.start()

        elif self.state == self.actions.walk:
            if collisions_all.fall:
                self.state = self.actions.fall.start()
            elif new_action:
                self.state = self.actions.from_class(new_action).start()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == self.actions.fall:
            if collisions_all.fall:
                self.actions.fall.run()
            elif self.actions.fall.dead:
                self.state = self.actions.dead.start()
            else:
                self.actions.fall.clamp()
                self.state = self.actions.walk.start()

        elif self.state == self.actions.float:
            if collisions_all.fall:
                self.actions.float.run()
            elif self.actions.float.enabled:
                self.state = self.actions.walk.start()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == self.actions.stop:
            self.actions.stop.run()

        elif self.state == self.actions.bomb:
            if self.actions.bomb.timer.finished or collisions_all.fall:
                self.actions.bomb.run()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == self.actions.build:
            if self.actions.build.finished or collisions_bg.side:
                self.state = self.actions.walk.start()
            else:
                self.actions.build.run()

        elif self.state == self.actions.digv:
            if (not collisions_bg.fall) and (not collisions_bg.outside):
                self.actions.digv.run()
            else:
                self.state = self.actions.walk.start()

        elif self.state == self.actions.digh:
            if (
                collisions_bg.side
                and (not collisions_bg.fall)
                and (not collisions_bg.outside)
            ):
                self.actions.digh.run()
            elif collisions_all.fall or self.actions.digh.enabled:
                self.state = self.actions.walk.start()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == self.actions.mine:
            if (
                collisions_bg.side
                and (not collisions_bg.fall)
                and (not collisions_bg.outside)
            ):
                self.actions.mine.run()
            elif collisions_all.fall or self.actions.mine.enabled:
                self.state = self.actions.walk.start()
            else:
                self.actions.walk.run(collisions_all)

        elif self.state == self.actions.dead:
            self.actions.dead.run()

        retro.AnimatedSprite.update(self)

    def draw_bg(self):
        if self.state != self.actions.stop: return

        retro.AnimatedSprite.draw(self, self.bg.image)

    def draw_screen(self):
        if self.state == self.actions.stop: return
        elif self.state == self.actions.bomb:
            self.actions.bomb.draw_timer()

        retro.AnimatedSprite.draw(self, self.window)
