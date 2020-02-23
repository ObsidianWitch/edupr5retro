import shared.retro as retro
from shooter.path import asset
from shooter.nodes.enemy import Enemy

class Runner(Enemy):
    RUNNER_IMG = retro.Image.from_path(
        asset("bandit_street3.png"),
    )

    def __init__(self, camera):
        Enemy.__init__(self, camera, self.RUNNER_IMG)
        self.dx = -2

    def move(self):
        self.rect.x += self.dx

        if self.camera.bg.rect.contains(self.rect): return

        self.dx *= -1
        self.flip(xflip = True)
        self.rect.clamp(self.camera.bg.rect)

    def update(self, target):
        Enemy.update(self, target)
        self.move()
