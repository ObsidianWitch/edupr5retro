import types
from retro.src import retro
from lemmings.nodes.actions import Actions
from lemmings.path import asset

class Lemming(retro.Sprite):
    IMG = retro.Image(asset("lemming.png"))

    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        revrange = lambda start, end: range(end - 1, start - 1, -1)
        retro.Sprite.__init__(
            self       = self,
            image      = self.IMG,
            animations = retro.Animations(
                frame_size = (30, 30),
                period = 100,
                WALK_L  = (range(0, 8), 0),   WALK_R  = (revrange(0, 8), 12),
                WALKA_L = (range(0, 8), 11),  WALKA_R = (revrange(0, 8), 23),
                FALL_L  = (range(0, 4), 1),   FALL_R  = (revrange(0, 4), 13),
                FLOAT_L = (range(0, 6), 3),   FLOAT_R = (revrange(0, 6), 15),
                STOP_L  = (range(0, 16), 4),  STOP_R  = (revrange(0, 16), 16),
                BOMB_L  = (range(0, 14), 5),  BOMB_R  = (revrange(0, 14), 17),
                BUILD_L = (range(0, 16), 6),  BUILD_R = (revrange(0, 16), 18),
                DIGV_L  = (range(0, 16), 7),  DIGV_R  = (revrange(0, 16), 19),
                DIGH_L  = (range(0, 12), 8),  DIGH_R  = (revrange(0, 12), 20),
                MINE_L  = (range(0, 17), 9),  MINE_R  = (revrange(0, 17), 21),
                DEAD_L  = (range(0, 16), 10), DEAD_R  = (revrange(0, 16), 22),
            ),
        )
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
        directions = retro.Collisions.pixel_mid(
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
                self.actions.walk.run(collisions_all, pending_action=True)

        elif self.state == self.actions.stop:
            self.actions.stop.run()

        elif self.state == self.actions.bomb:
            if self.actions.bomb.timer.finished or collisions_all.fall:
                self.actions.bomb.run()
            else:
                self.actions.walk.run(collisions_all, pending_action=True)

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
                self.actions.walk.run(collisions_all, pending_action=True)

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
                self.actions.walk.run(collisions_all, pending_action=True)

        elif self.state == self.actions.dead:
            self.actions.dead.run()

    def draw_bg(self):
        if self.state == self.actions.stop:
            retro.Sprite.draw(self, self.bg.image)

    def draw_screen(self):
        if self.state == self.actions.stop: return
        elif self.state == self.actions.bomb:
            self.actions.bomb.draw_timer()

        retro.Sprite.draw(self, self.window)
