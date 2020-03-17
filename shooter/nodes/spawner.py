import random
import shared.retro as retro
from shared.sprite import Sprite
from shooter.nodes.enemy import Enemy
from shooter.nodes.kidnaper import Kidnaper
from shooter.nodes.runner import Runner
from shooter.path import asset

class Spawner:
    STREET_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset("bandit_street1.png"),
        asset("bandit_street2.png"),
        asset("bandit_street4.png"),
    ))

    WINDOW_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset("bandit_window1.png"),
        asset("bandit_window2.png"),
        asset("bandit_window3.png"),
        asset("bandit_window4.png"),
    ))

    WALL_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset("bandit_wall1.png"),
        asset("bandit_wall2.png"),
    ))

    TOP_IMGS = tuple(retro.Image.from_path(p) for p in (
        asset("bandit_support1.png"),
        asset("bandit_support2.png"),
        asset("bandit_support3.png"),
    ))

    SEWER_IMG = retro.Image.from_path(
        asset("bandit_sewer.png"),
    )

    def __init__(self, stage):
        self.stage = stage

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
        self.repop_timer = retro.Counter(3)

    def street_position(self, sprite):
        sprite.rect.x = random.randint(100, 1900)
        sprite.rect.bottom = 676

    def new_street_mob(self):
        mob = Enemy(random.choice(self.STREET_IMGS))
        self.street_position(mob)
        return mob

    def new_window_mob(self):
        i = random.randrange(len(self.WINDOW_IMGS))
        positions = ((1244, 78), (1312, 258), (952, 84), (790, 88))
        mob = Enemy(self.WINDOW_IMGS[i])
        mob.rect.topleft = positions[i]
        return mob

    def new_wall_mob(self):
        positions = ((710, 600), (1140, 600), (1823, 600))
        mob = Enemy(random.choice(self.WALL_IMGS))
        mob.rect.bottomright = random.choice(positions)
        return mob

    def new_top_mob(self):
        positions = ((29, 191), (356, 191), (1712, 411))
        mob = Enemy(random.choice(self.TOP_IMGS))
        mob.rect.midbottom = random.choice(positions)
        return mob

    def new_sewer_mob(self):
        mob = Enemy(self.SEWER_IMG)
        mob.rect.topleft = (410, 642)
        return mob

    def new_kidnaper_mob(self):
        mob = Kidnaper()
        self.street_position(mob)
        return mob

    def new_runner_mob(self):
        mob = Runner(self.stage)
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
