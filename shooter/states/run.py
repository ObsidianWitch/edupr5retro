import shared.retro as retro
from shared.background import Background
from shared.sprite import Sprite
from shooter.nodes.spawner import Spawner
from shooter.nodes.player import Player
from shooter.path import asset
from shooter.camera import Camera
from shooter.hints  import Hints

class StateRun:
    def __init__(self, window):
        self.window = window

        self.bg = Background(asset("map.png"))

        self.camera = Camera(
            window   = self.window,
            bg       = self.bg,
            position = (350, 170),
        )

        self.player  = Player(self.camera)
        self.spawner = Spawner(self.camera)
        self.hints   = Hints(self.camera)

    @property
    def finished(self):
        return (self.player.ammunitions.count <= 0)

    def run(self):
        # Update
        self.player.update(self.spawner)
        self.spawner.update(self.player)

        # Draw
        ## bg drawing
        self.bg.clear()
        self.spawner.mob.draw(self.bg.current)
        self.player.explosions.draw(self.bg.current)

        ## screen drawing
        self.window.draw_img(
            img  = self.bg.current,
            pos  = (0, 0),
            area = self.camera.rect,
        )
        self.player.crosshair.draw(self.window)
        self.player.hide.draw(self.window)
        self.player.ammunitions.draw(self.window)
        self.spawner.mob.draw_shoot_timer(self.window)
        self.hints.draw(self.player, self.spawner.mob, self.window)
