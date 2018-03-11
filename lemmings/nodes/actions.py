import enum
import include.retro as retro
from shared.timer import Timer
from shared.sprite import Sprite
from lemmings.path import asset_path

STATES = enum.Enum("STATES", """START WALK FALL FLOAT STOP BOMB
                                BUILD DIGV DIGH MINE DEAD""")

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming
        self.dx = 0

    def start(self):
        self.dx = -1

    def run(self, collisions):
        if collisions.side:
            self.dx *= -1
            self.lemming.rect.move(-self.dx * 20, 0)

        self.lemming.set_animation("WALK")
        self.lemming.rect.move(self.dx, 0)
        self.slope()

    def slope(self):
        up = self.slope_up()
        if not up: self.slope_down()

    def slope_up(self):
        self.lemming.rect.move(0, -2)
        c = self.lemming.collisions(self.lemming.bg.current)
        if c.fall: self.lemming.rect.move(0, 2)
        return (not c.fall)

    def slope_down(self):
        c = self.lemming.collisions(self.lemming.bg.current)
        if c.fall: self.lemming.rect.move(0, 2)

        c = self.lemming.collisions(self.lemming.bg.current)
        if c.fall: self.lemming.rect.move(0, -2)

class Fall:
    def __init__(self, lemming):
        self.lemming = lemming

    @property
    def dead(self): return (self.fallcount >= 100)

    def start(self):
        self.lemming.start_animation("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.rect.move(0, 3)
        self.fallcount += 3

    def clamp(self):
        self.lemming.rect.move(0, -1)
        c = self.lemming.collisions(self.lemming.bg.current)
        if c.fall: self.lemming.rect.move(0, 1)
        else: self.clamp()

class Float:
    ICON  = retro.Image.from_path(asset_path("ui_float.png"))
    STATE = STATES.FLOAT

    def __init__(self, lemming):
        self.lemming = lemming

    def wait(self):
        self.enabled = False

    def start(self):
        self.lemming.start_animation("FLOAT")
        self.enabled = True

    def run(self):
        if not self.enabled: self.start()
        self.lemming.rect.move(0, 1)

class Stop:
    ICON  = retro.Image.from_path(asset_path("ui_stop.png"))
    STATE = STATES.STOP

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("STOP")

    def run(self): pass

class Bomb:
    ICON = retro.Image.from_path(asset_path("ui_bomb.png"))
    STATE = STATES.BOMB

    def __init__(self, lemming):
        self.lemming = lemming

    def wait(self):
        self.timer = Timer(end = 3, period = 1000)
        self.explode = False

    def start(self):
        self.lemming.start_animation("BOMB")
        self.explode = True

        self.lemming.bg.original.draw_circle(
            color  = retro.BLACK,
            center = self.lemming.bounding_rect.midbottom,
            radius = 20,
        )

    def run(self):
        if not self.lemming.animations.finished: return
        self.lemming.kill()

    def draw_timer(self):
        if self.explode: return

        window = self.lemming.window
        timer_surface = Sprite(window.fonts[0].render(
            text  = f"{self.timer.remaining}",
            color = retro.WHITE,
        ))
        timer_surface.rect.midbottom = self.lemming.bounding_rect.midtop
        timer_surface.draw(window)

class Build:
    ICON  = retro.Image.from_path(asset_path("ui_build.png"))
    STATE = STATES.BUILD

    def __init__(self, lemming):
        self.lemming = lemming
        self.count = 0

    @property
    def finished(self): return (self.count >= 12)

    def start(self):
        self.lemming.start_animation("BUILD")

    def run(self):
        if not self.lemming.animations.finished: return

        dx = self.lemming.actions.walk.dx
        rect = self.lemming.rect.copy()
        rect.size = (15, 3)
        rect.top = self.lemming.rect.bottom - rect.height
        if   (dx > 0): rect.left = self.lemming.rect.right - (rect.width // 2)
        elif (dx < 0): rect.left  -= rect.width // 2

        self.lemming.bg.original.draw_rect(
            color = (125, 125, 125), # grey
            rect  = rect,
        )

        self.lemming.rect.move(dx * rect.width // 2, -rect.height)

        self.count += 1
        self.lemming.start_animation("BUILD")

class DigV:
    ICON  = retro.Image.from_path(asset_path("ui_digv.png"))
    STATE = STATES.DIGV

    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("DIGV")

    def run(self):
        dx = self.lemming.actions.walk.dx

        rect = self.lemming.rect.copy()
        rect.top = rect.bottom - 1
        rect.left += 10 if dx > 0 else 0
        rect.size = (20, 2)

        self.lemming.bg.original.draw_rect(retro.BLACK, rect)
        self.lemming.rect.move(0, 1)

class DigH:
    ICON  = retro.Image.from_path(asset_path("ui_digh.png"))
    STATE = STATES.DIGH

    def __init__(self, lemming):
        self.lemming = lemming

    def wait(self):
        self.enabled = False

    def start(self):
        self.lemming.start_animation("DIGH")
        self.enabled = True

    def run(self):
        if not self.enabled: self.start()

        dx = self.lemming.actions.walk.dx

        rect = self.lemming.rect.copy()
        rect.left = rect.right - 15 if dx > 0 else rect.left - 1
        rect.width = 16


        self.lemming.bg.original.draw_rect(retro.BLACK, rect)
        self.lemming.rect.move(dx, 0)

class Mine:
    ICON  = retro.Image.from_path(asset_path("ui_mine.png"))
    STATE = STATES.MINE

    def __init__(self, lemming):
        self.lemming = lemming

    def wait(self):
        self.enabled = False

    def start(self):
        self.lemming.start_animation("MINE")
        self.enabled = True

    def run(self):
        if not self.enabled: self.start()
        if not self.lemming.animations.finished: return

        self.lemming.bg.original.draw_circle(
            color  = retro.BLACK,
            center = self.lemming.rect.center,
            radius = 18,
        )

        dx = self.lemming.actions.walk.dx
        self.lemming.rect.move(3 * dx, 3)
        self.lemming.start_animation("MINE")

class Dead:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.start_animation("DEAD")

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
