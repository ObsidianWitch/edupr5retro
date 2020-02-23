import shared.retro as retro
from shared.stage import Stage
from shared.sprite import Sprite
from shooter.nodes.spawner import Spawner
from shooter.nodes.player import Player
from shooter.path import asset

class StateRun:
    def __init__(self, window):
        self.window = window

        self.stage = Stage(asset("map.png"))
        self.stage.camera = self.window.rect()
        self.stage.camera.move(350, 170)

        self.player = Player(self.window, self.stage)
        self.spawner = Spawner(self.stage)

    @property
    def finished(self):
        return (self.player.ammunitions.count <= 0)

    def run(self):
        # Update
        self.player.update(self.spawner)
        self.spawner.update(self.player)

        # Draw
        ## bg drawing
        self.stage.clear_focus()
        self.spawner.mob.draw(self.stage.image)
        self.player.explosions.draw(self.stage.image)

        ## screen drawing
        self.window.draw_img(
            img  = self.stage.image,
            pos  = (0, 0),
            area = self.stage.camera,
        )
        self.player.crosshair.draw(self.window)
        self.player.hide.draw(self.window)
        self.player.ammunitions.draw(self.window)
        self.player.hints.draw(self.player, self.spawner.mob, self.window)
        self.spawner.mob.draw_shoot_timer(self.window.fonts[1], self.window)
