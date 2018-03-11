import random
import include.retro as retro
from shared.sprite import Sprite
from shared.timer import Timer
from empire_city.nodes.enemies.enemy import Enemy
from empire_city.nodes.enemies.kidnaper import Kidnaper
from empire_city.nodes.enemies.runner import Runner
from empire_city.path import asset_path

# Enemy generator.
class Enemies:
    STREET_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset_path("bandit_rue.png"),
        asset_path("bandit_rue2.png"),
        asset_path("bandit_rue4.png"),
    ))

    WINDOW_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset_path("bandit_window.png"),
        asset_path("bandit_window2.png"),
        asset_path("bandit_window3.png"),
        asset_path("bandit_window4.png"),
    ))

    WALL_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset_path("bandit_mur.png"),
        asset_path("bandit_mur2.png"),
    ))

    TOP_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset_path("bandit_appui.png"),
        asset_path("bandit_appui2.png"),
        asset_path("bandit_appui3.png"),
    ))

    SEWER_IMG = retro.Image.from_path(
        asset_path("bandit_egout.png"),
    )

    KIDNAPER_IMG = retro.Image.from_path(
        asset_path("woman.png"),
    )

    RUNNER_IMG = retro.Image.from_path(
        asset_path("bandit_rue3.png"),
    )

    def __init__(self, camera):
        self.camera = camera
        self.bg = camera.bg

        self.generators = (
            self.new_street_mob,
            self.new_window_mob,
            self.new_wall_mob,
            self.new_top_mob,
            self.new_sewer_mob,
            self.new_kidnaper_mob,
            self.new_runner_mob,
        )
        self.next()
        self.mob.alive = False
        self.repop_timer = Timer(3)

    def street_position(self, sprite):
        sprite.rect.bottom = self.bg.rect.bottom - 10
        sprite.rect.left = random.randint(100, self.bg.rect.width - 100)

    def new_street_mob(self):
        mob = Enemy(self.camera, random.choice(self.STREET_IMGS))
        self.street_position(mob)
        return mob

    def new_window_mob(self):
        i = random.randrange(len(self.WINDOW_IMGS))
        positions = ((1244, 78), (1312, 258), (952, 84), (790, 88))
        mob = Enemy(self.camera, self.WINDOW_IMGS[i])
        mob.rect.topleft = positions[i]
        return mob

    def new_wall_mob(self):
        positions = ((710, 600), (1140, 600), (1823, 600))
        mob = Enemy(self.camera, random.choice(self.WALL_IMGS))
        mob.rect.bottomright = random.choice(positions)
        return mob

    def new_top_mob(self):
        positions = ((29, 191), (356, 191), (1712, 411))
        mob = Enemy(self.camera, random.choice(self.TOP_IMGS))
        mob.rect.midbottom = random.choice(positions)
        return mob

    def new_sewer_mob(self):
        mob = Enemy(self.camera, self.SEWER_IMG)
        mob.rect.topleft = (410, 642)
        return mob

    def new_kidnaper_mob(self):
        mob = Kidnaper(self.camera, self.KIDNAPER_IMG)
        self.street_position(mob)
        return mob

    def new_runner_mob(self):
        mob = Runner(self.camera, self.RUNNER_IMG)
        self.street_position(mob)
        return mob

    def next(self):
        self.mob = random.choice(self.generators)()

    def kill(self, p):
        killed = self.mob.kill(p)
        if killed: self.repop_timer.restart()
        return killed

    def update(self, target):
        repop = (
            not self.mob.alive
            and self.repop_timer.finished
        )
        if repop: self.next()

        self.mob.update(target)

    def draw_bg(self):
        self.mob.draw_bg()

    def draw_screen(self):
        self.mob.draw_screen()
