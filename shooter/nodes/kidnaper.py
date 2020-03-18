from retro.out import retro
from shooter.path import asset
from shooter.nodes.enemy import Enemy

class Kidnaper(Enemy):
    KIDNAPER_IMG = retro.Image.from_path(
        asset("bandit_kidnaper.png"),
    )

    def __init__(self):
        Enemy.__init__(self, self.KIDNAPER_IMG)

    def kill(self, p):
        kidnaper = self.rect.copy()
        kidnaper.width //= 2
        victim = self.rect.copy()
        victim.width //= 2
        victim.x += victim.width

        victim_killed   = (self.alive and victim.collidepoint(p))
        kidnaper_killed = (self.alive and kidnaper.collidepoint(p))
        if victim_killed or kidnaper_killed: self.alive = False
        return (kidnaper_killed - victim_killed)
