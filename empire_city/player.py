from empire_city.common import asset_path
from shared.sprite import Sprite
import shared.math

class Player:
    def __init__(self, window):
        self.window = window

        self.speed = 10

        self.crosshair = Sprite.from_paths([asset_path("viseur.png")])
        self.crosshair.rect.center = window.rect.center

    def move(self, move_vec, collisions_vec):
        for i,_ in enumerate(move_vec):
            move_vec[i] -= collisions_vec[i]
            move_vec[i] = shared.math.clamp(move_vec[i], -1, 1)

        self.crosshair.rect.move_ip(
            move_vec[0] * self.speed,
            move_vec[1] * self.speed,
        )

    def draw(self):
        self.window.screen.blit(self.crosshair.image, self.crosshair.rect)
