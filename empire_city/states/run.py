import pygame

from shared.background import Background
from shared.sprite import Sprite
from empire_city.nodes.enemies.enemies import Enemies
from empire_city.nodes.player import Player
from empire_city.path import asset_path
from empire_city.camera import Camera
from empire_city.hints  import Hints


class StateRun:
    def __init__(self, window):
        self.window = window

        self.bg = Background(asset_path("map.png"))

        self.camera = Camera(
            window   = self.window,
            bg       = self.bg,
            position = (350, 170),
        )

        self.player  = Player(self.camera)
        self.enemies = Enemies(self.camera)
        self.hints   = Hints(self.camera)

        self.end = False

    def run(self):
        # Update
        scroll_vec = self.camera.scroll_zone_collide(
            self.player.crosshair.rect.center
        ).vec
        self.camera.update(scroll_vec)
        self.player.update(scroll_vec, self.enemies)
        self.enemies.update(self.player)

        self.end = (self.player.ammunitions.count <= 0)

        # Draw
        ## bg drawing
        self.bg.clear()
        self.enemies.draw_bg()
        self.player.draw_bg()

        ## screen drawing
        self.window.screen.blit(
            source = self.bg.current,
            dest   = self.bg.rect,
            area   = self.camera.display_zone
        )
        self.player.draw_screen()
        self.enemies.draw_screen()
        self.hints.draw_screen(self.player, self.enemies.mob)

        return False
