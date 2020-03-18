import shared.retro as retro
from lemmings.path import asset

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming
        self.dx = -1

    def start(self):
        return self

    def run(self, collisions):
        self.walk(collisions)
        self.slope()

    def walk(self, collisions):
        if collisions.side:
            self.dx *= -1
            self.lemming.rect.move_ip(-self.dx * 20, 0)

        self.lemming.set_animation("WALK")
        self.lemming.rect.move_ip(self.dx, 0)

    def slope(self):
        c = self.lemming.collisions(self.lemming.bg.image)
        if not c.fall: self.slope_up()
        else:          self.slope_down()

    def slope_up(self):
        self.lemming.rect.move_ip(0, -2)
        c = self.lemming.collisions(self.lemming.bg.image)
        if c.fall: self.lemming.rect.move_ip(0, 2)

    def slope_down(self):
        self.lemming.rect.move_ip(0, 2)
        c = self.lemming.collisions(self.lemming.bg.image)
        if c.fall: self.lemming.rect.move_ip(0, -2)

class Fall:
    def __init__(self, lemming):
        self.lemming = lemming

    @property
    def dead(self): return (self.fallcount >= 100)

    def start(self):
        self.lemming.start_animation("FALL")
        self.fallcount = 0
        return self

    def run(self):
        self.lemming.rect.move_ip(0, 3)
        self.fallcount += 3

    def clamp(self):
        self.lemming.rect.move_ip(0, -1)
        c = self.lemming.collisions(self.lemming.bg.image)
        if c.fall: self.lemming.rect.move_ip(0, 1)
        else: self.clamp()

class Float:
    ICON  = retro.Image.from_path(asset("ui_float.png"))

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.enabled = False
        return self

    def run(self):
        if not self.enabled:
            self.lemming.start_animation("FLOAT")
            self.enabled = True
        self.lemming.rect.move_ip(0, 1)

class Stop:
    ICON  = retro.Image.from_path(asset("ui_stop.png"))

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("STOP")
        return self

    def run(self):
        pass

class Bomb:
    ICON = retro.Image.from_path(asset("ui_bomb.png"))

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.timer = retro.Counter(end = 3, period = 1000)
        self.explode = False
        return self

    def run(self):
        if not self.explode:
            self.lemming.start_animation("BOMB")
            self.explode = True

            self.lemming.bg.original.draw_circle(
                color  = retro.BLACK,
                center = self.lemming.bounding_rect.midbottom,
                radius = 20,
            )
        elif self.lemming.animations.finished:
            self.lemming.kill()

    def draw_timer(self):
        if self.explode: return

        window = self.lemming.window
        timer_surface = retro.Sprite(window.fonts[0].render(
            text  = f"{self.timer.remaining}",
            color = retro.WHITE,
        ))
        timer_surface.rect.midbottom = self.lemming.bounding_rect.midtop
        timer_surface.draw(window)

class Build:
    ICON  = retro.Image.from_path(asset("ui_build.png"))

    def __init__(self, lemming):
        self.lemming = lemming
        self.count = 0

    @property
    def finished(self): return (self.count >= 12)

    def start(self):
        self.lemming.start_animation("BUILD")
        return self

    def run(self):
        if not self.lemming.animations.finished: return

        dx = self.lemming.actions.walk.dx
        rect = self.lemming.rect.copy()
        rect.size = (15, 3)
        rect.top = self.lemming.rect.bottom - rect.height
        if   (dx > 0): rect.left = self.lemming.rect.right - (rect.width // 2)
        elif (dx < 0): rect.left  -= rect.width // 2

        self.lemming.bg.original.draw_rect(retro.GREY, rect)

        self.lemming.rect.move_ip(dx * rect.width // 2, -rect.height)

        self.count += 1
        self.lemming.start_animation("BUILD")

class DigV:
    ICON  = retro.Image.from_path(asset("ui_digv.png"))

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("DIGV")
        return self

    def run(self):
        dx = self.lemming.actions.walk.dx

        rect = self.lemming.rect.copy()
        rect.top = rect.bottom - 1
        rect.left += 10 if dx > 0 else 0
        rect.size = (20, 2)

        self.lemming.bg.original.draw_rect(retro.BLACK, rect)
        self.lemming.rect.move_ip(0, 1)

class DigH:
    ICON  = retro.Image.from_path(asset("ui_digh.png"))

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.enabled = False
        return self

    def run(self):
        if not self.enabled:
            self.lemming.start_animation("DIGH")
            self.enabled = True

        dx = self.lemming.actions.walk.dx

        rect = self.lemming.rect.copy()
        rect.left = rect.right - 15 if dx > 0 else rect.left - 1
        rect.width = 16


        self.lemming.bg.original.draw_rect(retro.BLACK, rect)
        self.lemming.rect.move_ip(dx, 0)

class Mine:
    ICON  = retro.Image.from_path(asset("ui_mine.png"))

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.enabled = False
        return self

    def run(self):
        if not self.enabled:
            self.lemming.start_animation("MINE")
            self.enabled = True

        if not self.lemming.animations.finished:
            return

        self.lemming.bg.original.draw_circle(
            color  = retro.BLACK,
            center = self.lemming.rect.center,
            radius = 18,
        )

        dx = self.lemming.actions.walk.dx
        self.lemming.rect.move_ip(3 * dx, 3)
        self.lemming.start_animation("MINE")

class Dead:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("DEAD")
        return self

    def run(self):
        if self.lemming.animations.finished: self.lemming.kill()

class Actions:
    USABLE = (Float, Stop, Bomb, Build, DigV, DigH, Mine)

    def __init__(self, lemming):
        self.walk  = Walk(lemming)
        self.fall  = Fall(lemming)
        self.float = Float(lemming)
        self.stop  = Stop(lemming)
        self.bomb  = Bomb(lemming)
        self.build = Build(lemming)
        self.digv  = DigV(lemming)
        self.digh  = DigH(lemming)
        self.mine  = Mine(lemming)
        self.dead  = Dead(lemming)
        self.lst = (
            self.walk, self.fall, self.float, self.stop, self.bomb,
            self.build, self.digv, self.digh, self.mine, self.dead,
        )

    def from_class(self, cls):
        return next(action for action in self.lst if type(action) == cls)
