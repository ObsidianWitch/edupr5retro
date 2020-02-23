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
        scroll_vec = self.camera.scroll_zone_collide(
            self.player.crosshair.rect.center
        ).vec
        self.camera.update(scroll_vec)
        self.player.update(scroll_vec, self.spawner)
        self.spawner.update(self.player)

        # Draw
        ## bg drawing
        self.bg.clear()
        self.spawner.draw_bg()
        self.player.draw_bg()

        ## screen drawing
        self.window.draw_img(
            img  = self.bg.current,
            pos  = self.bg.rect,
            area = self.camera.display_zone,
        )
        self.player.draw_screen()
        self.spawner.draw_screen()
        self.hints.draw_screen(self.player, self.spawner.mob)
