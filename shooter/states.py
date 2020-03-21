from retro.src import retro
from shooter.nodes.spawner import Spawner
from shooter.nodes.player import Player
from shooter.path import asset

class Run:
    def __init__(self, window):
        self.window = window

        self.stage = retro.Stage(asset("map.png"))
        self.stage.camera = self.window.rect()
        self.stage.camera.move_ip(350, 170)

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
        self.stage.draw(self.window)
        self.player.crosshair.draw(self.window)
        self.player.hide.draw(self.window)
        self.player.ammunitions.draw(self.window)
        self.player.hints.draw(self.player, self.spawner.mob, self.window)
        self.spawner.mob.draw_shoot_timer(self.window.fonts[1], self.window)

class End:
    def __init__(self, window):
        self.window = window
        self.restart = False

        self.txt = retro.Sprite(self.window.fonts[4].render(
            text    = "DEAD",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        self.txt.rect.center = self.window.rect().center

    def run(self):
        # Update
        key = self.window.events.key_press
        self.restart = key(retro.K_SPACE)

        # Draw
        self.txt.draw(self.window)
